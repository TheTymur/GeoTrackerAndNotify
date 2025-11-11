from GUI import MyGeoTrackerUI, setup_Reminder_screen, ErrorNotify
from . import location_getter_api
import threading
import time
from . import reminder_repository
from datetime import datetime
from pathlib import Path

__all__ = ["Event_manager"]

saved_reminders_path = Path(r"C:\Python\GeoTrackerAndNotify\saved_reminders\saved_reminders.db")

class Event_manager:
    def __init__(self, main_window):
        self.reminder_window = None
        self.reminder_repo = reminder_repository.RemindersRepositoryORM(saved_reminders_path)
        self.main = main_window
        self.error_notify = ErrorNotify()
        threading.Thread(target=self.background_update_location, daemon=True).start()
        

    def open_create_reminder_window(self):
        if self.reminder_window is None:
            self.reminder_window = setup_Reminder_screen()
            self.reminder_window.destroyed.connect(self._on_reminder_closed)

            self.reminder_window.cancel_button.clicked.connect(self.reminder_window.close)
            self.reminder_window.save_button.clicked.connect(self.save_new_reminder)

        self.reminder_window.input_address.clear()
        self.reminder_window.input_reminderName.clear()
        self.reminder_window.input_date.clear()


        self.reminder_window.show()
        self.reminder_window.raise_()
        self.reminder_window.activateWindow()
    

    def get_all_reminder(self):
        print(self.reminder_repo.get_all())

    def _on_reminder_closed(self):
        self.reminder_window = None

    def background_update_location(self):
        while True:
            if location_getter_api.address is None:
                address = "Unknown"
            else:
                address = location_getter_api.address

            self.main.set_location(address)

            time.sleep(300)


    def save_new_reminder(self):
        current_address = location_getter_api.address
        name_of_reminder = self.reminder_window.input_reminderName.text().strip()
        address = self.reminder_window.input_address.text().strip()
        date_of_reminder = self.reminder_window.input_date.text().strip()

        date_format = "%d.%m.%Y"

        try:
            parsed_date_object = datetime.strptime(date_of_reminder, date_format).date()

        except ValueError:
            self.error_notify.show_error(f"The date '{date_of_reminder}' is not in the correct format (DD.MM.YYYY).")
            return

        if current_address is None:
            self.error_notify.show_error("Warning!\n Your current location is unknown!")
        
        new_reminder = {
            "name": name_of_reminder,
            "address": current_address if not address else address,
            "date": parsed_date_object
        }

        self.reminder_repo.add_reminder(new_reminder)
        self.reminder_window.close()
        
 
    def create_reminder_signal_connection(self, main_window: MyGeoTrackerUI):
        main_window.button_createReminder.clicked.connect(self.open_create_reminder_window)
        main_window.button_getAll.clicked.connect(self.get_all_reminder)
        

