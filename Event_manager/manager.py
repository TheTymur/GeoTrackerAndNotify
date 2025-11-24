from GUI import MyGeoTrackerUI, ErrorNotify, PermissionRequest, setupReminderScreen
from . import location_service
from PyQt5.QtCore import QObject, pyqtSignal
import threading
import time
from . import reminder_repository
from datetime import datetime
import webbrowser

__all__ = ["EventManager"]

saved_reminders_path = "./saved_reminders/saved_reminders.db"

class EventManager(QObject):

    location_updated = pyqtSignal(str)

    def __init__(self, main_window):
        super().__init__()
        self.reminder_window = None
        self.reminder_repo = reminder_repository.RemindersRepositoryORM(saved_reminders_path)
        self.main = main_window
        self.error_notify = ErrorNotify()
        self.permission_requesting()


    def permission_requesting(self):    
        permission_box = PermissionRequest()
        msg = "Would you like to give permission for geolocation?"
        user_said_yes = permission_box.show_requestbox(msg)

        print(user_said_yes)
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
        
        new_reminder = {
            "name": name_of_reminder,
            "address": current_address if not address else address,
            "date": parsed_date_object,
            "time": parsed_time_object
        }

        self.reminder_repo.add_reminder(new_reminder)
        self.reminder_window.close()
        self.get_all_reminder()
        
 
    def create_reminder_signal_connection(self, main_window: MyGeoTrackerUI):
        main_window.button_createReminder.clicked.connect(self.open_create_reminder_window)
        main_window.button_getAll.clicked.connect(self.get_all_reminder)
        

