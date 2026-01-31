from GUI import MyGeoTrackerUI, ErrorNotify, PermissionRequest, setupReminderScreen
from . import location_service
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import QMessageBox
import threading
import time
from . import reminder_repository
from datetime import datetime
import webbrowser

__all__ = ["EventManager"]

saved_reminders_path = "./saved_reminders/saved_reminders.db"

class EventManager(QObject):

    location_updated = pyqtSignal(str)
    reminder_repo = reminder_repository.RemindersRepositoryORM(saved_reminders_path)

    def __init__(self, main_window):
        super().__init__()
        self.reminder_window = None
        self.main = main_window
        self.error_notify = ErrorNotify()
        self.permission_requesting()
        self.current_editing_id = None
        self.get_all_reminder()        


    def permission_requesting(self):    
        permission_box = PermissionRequest()
        msg = "Would you like to give permission for geolocation?"
        user_said_yes = permission_box.show_requestbox(msg)

        if user_said_yes:
            self.main.set_location("Please wait... We are getting your location.")
            threading.Thread(target=self.background_update_location, daemon=True).start()
        else:
            self.main.set_location("Permission denied. Location tracking is off.")
        

    def open_create_reminder_window(self):
        if self.reminder_window is None:
            self.reminder_window = setupReminderScreen()
            self.reminder_window.destroyed.connect(self._on_reminder_closed)

            self.reminder_window.cancel_button.clicked.connect(self.reminder_window.close)
            self.reminder_window.save_button.clicked.connect(self.save_new_reminder)

        self.reminder_window.input_address.clear()
        self.reminder_window.input_reminderName.clear()
        self.reminder_window.input_date.clear()
        self.reminder_window.input_time.clear()


        self.reminder_window.show()
        self.reminder_window.raise_()
        self.reminder_window.activateWindow()

    def open_edit_reminder_window(self, reminder_id):
        self.current_editing_id = reminder_id
        reminder = self.reminder_repo.get_by_id(reminder_id)
        
        self.open_create_reminder_window()
        
        self.reminder_window.setWindowTitle("Edit Reminder")
        self.reminder_window.title.setText("Edit reminder")
        self.reminder_window.input_reminderName.setText(reminder.name)
        self.reminder_window.input_address.setText(reminder.address)
        self.reminder_window.input_date.setText(reminder.date.strftime("%d.%m.%Y"))
        self.reminder_window.input_time.setText(reminder.time.strftime("%H:%M"))
    

    def get_all_reminder(self):
        all_reminders = self.reminder_repo.get_all()
        self.main.update_reminder_list(all_reminders)

    def _on_reminder_closed(self):
        self.reminder_window = None

    def background_update_location(self):  
        url_to_open = "http://127.0.0.1:5000"
        webbrowser.open(url=url_to_open)
        self.address = None

        while self.address is None:
            time.sleep(1.0)
            self.address = location_service.address

        self.location_updated.emit(self.address)

        while True:            
            new_address = location_service.address

            if new_address != self.address:
                self.address = new_address
                if self.address is None:
                    self.address = "Unknown" 

                self.location_updated.emit(self.address)

            time.sleep(300)


    def save_new_reminder(self):
        current_address = location_service.address
        name_of_reminder = self.reminder_window.input_reminderName.text().strip()
        address = self.reminder_window.input_address.text().strip()
        date_of_reminder = self.reminder_window.input_date.text().strip()
        time_of_reminder = self.reminder_window.input_time.text().strip()

        date_format = "%d.%m.%Y"
        time_format = "%H:%M"

        try:
            parsed_date_object = datetime.strptime(date_of_reminder, date_format).date()

        except ValueError:
            self.error_notify.show_error(f"The date '{date_of_reminder}' is not in the correct format (DD.MM.YYYY).")
            return
        
        try:
            parsed_time_object = datetime.strptime(time_of_reminder, time_format).time()
        
        except ValueError:
            self.error_notify.show_error(f"The time '{time_of_reminder}' is not in the correct format (HH:MM).")
            return


        if current_address is None and address == "":
            self.error_notify.show_error("Warning!\n Your current location is unknown!")
            return
        
        reminder_data = {
            "name": name_of_reminder,
            "address": current_address if not address else address,
            "date": parsed_date_object,
            "time": parsed_time_object
        }

        if self.current_editing_id is not None:
            self.reminder_repo.update_reminder(self.current_editing_id, reminder_data)
            self.current_editing_id = None

        else:
            self.reminder_repo.add_reminder(reminder_data)

        self.reminder_window.close()
        self.get_all_reminder()

        
 
    def create_reminder_signal_connection(self, main_window: MyGeoTrackerUI):
        main_window.button_createReminder.clicked.connect(self.open_create_reminder_window)
        main_window.reminder_selected_signal.connect(self.handle_reminder_click)
        

    def handle_reminder_click(self, reminder_id):
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Manage Reminder")
        msg_box.setText("What would you like to do with this reminder?")

        edit_button = msg_box.addButton("Edit", QMessageBox.ActionRole)
        delete_button = msg_box.addButton("Delete", QMessageBox.DestructiveRole)
        cancel_button = msg_box.addButton(QMessageBox.Cancel)

        msg_box.exec_()

        if msg_box.clickedButton() == delete_button:
            self.reminder_repo.delete(reminder_id)
            self.get_all_reminder()

        if msg_box.clickedButton() == edit_button:
            self.open_edit_reminder_window(reminder_id)


