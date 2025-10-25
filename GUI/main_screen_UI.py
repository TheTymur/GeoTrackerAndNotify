import sys
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QGridLayout, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon

__all__ = ["MyGeoTrackerUI", "set_location"]

class MyGeoTrackerUI(QWidget):
    def __init__(self):
        super().__init__()
        self._setup_constants()
        self._setup_UI()
        

    def set_location(self, location_txt: str):
        self.location.setText(f"Location: {location_txt}")   
        
    def _setup_constants(self):
        self.font_header = QFont("Arial", 16, QFont.Bold)
        self.font_simple = QFont("Arial", 12)
        self.font_smaller_simple = QFont("Arial", 10)


    def _setup_UI(self):
        self.setWindowTitle("GeoTracker")
        self.setWindowIcon(QIcon("C:\Python\GeoTrackerAndNotify\GUI\Icons\GeoT.png"))
        self.resize(800, 800)

        self.layout = QGridLayout()
        self.title = QLabel("GeoTracker")
        self.title.setFont(self.font_header)
        self.location = QLabel("Location: Unknown")
        self.location.setFont(self.font_simple)
        self.button_createReminder = QPushButton("Create reminder")
        self.button_createReminder.setFont(self.font_smaller_simple)
        self.button_createReminder.setFixedSize(200,50)
        self.button_getAll = QPushButton("Get all reminders")
        self.button_getAll.setFont(self.font_smaller_simple)
        self.button_getAll.setFixedSize(200,50)

        self.layout.addWidget(self.title, 0,0,1,3, alignment=Qt.AlignTop | Qt.AlignHCenter)
        # self.title.setContentsMargins(50, 0, 0, 0) if I wanted to make some space from the sides
        self.layout.addItem(QSpacerItem(0, 80, QSizePolicy.Minimum, QSizePolicy.Fixed), 1, 0, 1, 3)
        self.layout.addWidget(self.location, 2,0,1,3, alignment=Qt.AlignHCenter | Qt.AlignTop)
        self.layout.addItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding), 3, 0, 1, 3)
        self.layout.addWidget(self.button_createReminder, 4,0,1,3, alignment= Qt.AlignRight)
        self.layout.addWidget(self.button_getAll, 4,0,1,2, alignment=Qt.AlignLeft)
        self.setLayout(self.layout)





