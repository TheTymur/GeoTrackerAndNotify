from PyQt5.QtWidgets import QSystemTrayIcon
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QObject

__all__ = ["NotificationUI"]

class NotificationUI(QObject):
    def __init__(self):
        super().__init__()

        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon(r"./assets/Icons/GeoT.png"))
        self.tray_icon.setVisible(True)



