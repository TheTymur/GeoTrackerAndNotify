from PyQt5.QtWidgets import QSystemTrayIcon
from GUI import NotificationUI
from . import location_service
from datetime import datetime
import time
from . import reminder_repository

saved_reminders_path = "./saved_reminders/saved_reminders.db"


class NotificationLogic():

    reminder_repo = reminder_repository.RemindersRepositoryORM(saved_reminders_path)

    def __init__(self, main_window):
        self.main_window = main_window
        self.notification_UI = NotificationUI()

    def _send_notification(self, title, message=""):
        icon_type = QSystemTrayIcon.Information
        duration = 3000

        self.notification_UI.tray_icon.showMessage(title, message, icon_type, duration)

    def _location_check(self, address_of_reminder):
        current_location = location_service.address
        
        if current_location is None:
            return False
        
        return current_location.strip() == address_of_reminder.strip()
        
    def _datetime_check(self, date_of_reminder, time_of_reminder_hours, time_of_reminder_minutes):
        current_date = datetime.now().strftime("%Y-%m-%d")
        current_time_hours = datetime.now().strftime("%H")
        current_time_minutes = datetime.now().strftime("%M")

        current_time = int(current_time_hours)*60 + int(current_time_minutes)
        time_of_reminder = int(time_of_reminder_hours)*60 + int(time_of_reminder_minutes)

        if current_date == date_of_reminder:
            if current_time >= time_of_reminder:
                return True
            
        return False
    def background_check(self):
        while True:

            all_reminders = self.reminder_repo.get_all()

            for reminder in all_reminders:

                if not reminder.time or not reminder.date:
                    continue

                time_of_reminder_hours = reminder.time.strftime("%H")
                time_of_reminder_minutes = reminder.time.strftime("%M")
                date_of_reminder = reminder.date.strftime("%Y-%m-%d")
                if self._datetime_check(date_of_reminder, time_of_reminder_hours, time_of_reminder_minutes) and self._location_check(reminder.address):
                    self._send_notification(f"{reminder.name}, reminding you!")            
            time.sleep(60)




    