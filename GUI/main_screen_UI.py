import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, 
                             QGridLayout, QSpacerItem, QSizePolicy, QScrollArea, 
                             QVBoxLayout, QFrame)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon
from pathlib import Path
__all__ = ["MyGeoTrackerUI", "set_location"] 
saved_reminders_path = Path(r"C:\Python\GeoTrackerAndNotify\saved_reminders\saved_reminders.db")

class ReminderWidget(QFrame):
    def __init__(self, reminder_text):
        super().__init__()
        self.setFrameShape(QFrame.StyledPanel)        
        self.layout = QVBoxLayout()
        self.label = QLabel(reminder_text)
        self.label.setFont(QFont("Arial", 11))
        
        self.label.setWordWrap(True)

        self.layout.addWidget(self.label)
        self.setLayout(self.layout)

class MyGeoTrackerUI(QWidget):
    def __init__(self):
        super().__init__()
        self._setup_constants()
        self._setup_UI()

    def set_location(self, location_address):
        self.location.setText(f"Location: {location_address}")
        
    def _setup_constants(self):
        self.font_header = QFont("Arial", 16, QFont.Bold)
        self.font_simple = QFont("Arial", 12)
        self.font_smaller_simple = QFont("Arial", 10)

    def _setup_UI(self):
        self.setWindowTitle("GeoTracker")
        self.setWindowIcon(QIcon(r"C:\Python\GeoTrackerAndNotify\GUI\Icons\GeoT.png"))
        self.resize(800, 800) 

        self.layout = QGridLayout()

        # Row 0
        self.title = QLabel("GeoTracker")
        self.title.setFont(self.font_header)
        self.layout.addWidget(self.title, 0, 0, 1, 3, alignment=Qt.AlignTop | Qt.AlignHCenter)

        # Row 1
        self.location = QLabel("Location: Unknown")
        self.location.setFont(self.font_simple)
        self.layout.addWidget(self.location, 1, 0, 1, 3, alignment=Qt.AlignHCenter)

        # Row 2
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("background-color: white;")

        # Container widget and layout for the scroll area's content
        self.scroll_content = QWidget()
        self.reminders_layout = QVBoxLayout(self.scroll_content) 
        self.reminders_layout.setAlignment(Qt.AlignTop)

        # Set the content widget into the scroll area
        self.scroll_area.setWidget(self.scroll_content)
        
        # Add the scroll area to the main grid
        self.layout.addWidget(self.scroll_area, 2, 0, 1, 3)

        # Row 3
        self.button_createReminder = QPushButton("Create reminder")
        self.button_createReminder.setFont(self.font_smaller_simple)
        self.button_createReminder.setFixedSize(200, 50)
        
        self.button_getAll = QPushButton("Get all reminders")
        self.button_getAll.setFont(self.font_smaller_simple)
        self.button_getAll.setFixedSize(200, 50)
        
        # Add buttons to Row 3, in separate columns for correct alignment
        self.layout.addWidget(self.button_getAll, 3, 0, alignment=Qt.AlignLeft)
        self.layout.addWidget(self.button_createReminder, 3, 2, alignment=Qt.AlignRight)

        # Make Row 2 (the scroll area) expand vertically
        self.layout.setRowStretch(2, 1) 
        
        # Make Column 1 (the middle) expand horizontally, pushing buttons apart
        self.layout.setColumnStretch(1, 1)

        self.setLayout(self.layout)

    def update_reminder_list(self, reminders_list):

        while self.reminders_layout.count():
            child = self.reminders_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        for reminder in reminders_list:
            text = f"ID: {reminder.id} <b> {reminder.name} </b> <br>At: {reminder.address}"
            new_widget = ReminderWidget(text)
            self.reminders_layout.addWidget(new_widget)        

        



