from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import QSystemTrayIcon
from GUI import NotificationUI, MyGeoTrackerUI


class NotificationLogic():
    def __init__(self, main_window):
        self.main_window = main_window
        self.notification_UI = NotificationUI()

    def _send_notification(self, title, message):
        icon_type = QSystemTrayIcon.Information
        duration = 3000

        self.notification_UI.tray_icon.showMessage(title, message, icon_type, duration)
        print("Sent")

    def send(self):
        self._send_notification("Test", "Testing... 1,2,3")

    def connect_signals(self):
        self.main_window.button_getAll.clicked.connect(self.send)

    