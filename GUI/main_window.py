import sys
from PyQt5.QtWidgets import (QWidget, QLabel, QPushButton, 
                             QGridLayout, QScrollArea, 
                             QVBoxLayout, QFrame)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QIcon
import datetime
from pathlib import Path
__all__ = ["MyGeoTrackerUI", "set_location"] 
saved_reminders_path = Path(r"./saved_reminders/saved_reminders.db")

class ReminderWidget(QFrame):
    clicked_signal = pyqtSignal(int)
    def __init__(self,reminder_id, reminder_text):
        super().__init__()
        self.setFrameShape(QFrame.StyledPanel)        
        self.layout = QVBoxLayout()
        self.reminder_id = reminder_id

        self.button_reminder = QPushButton()
        self.button_reminder.setMinimumHeight(80) 
        self.button_reminder.clicked.connect(lambda: self.clicked_signal.emit(self.reminder_id))
        
        button_internal_layout = QVBoxLayout(self.button_reminder)
        button_internal_layout.setContentsMargins(5, 5, 5, 5) 

        self.label = QLabel(reminder_text)
        self.label.setFont(QFont("Arial", 11))
        self.label.setWordWrap(True) 
        
        self.label.setAttribute(Qt.WA_TransparentForMouseEvents, True)

        button_internal_layout.addWidget(self.label)

        self.layout.addWidget(self.button_reminder)
        self.setLayout(self.layout)

class MyGeoTrackerUI(QWidget):

    reminder_selected_signal = pyqtSignal(int)

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
        self.setWindowIcon(QIcon(r"./assets/Icons/GeoT.png"))
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
        
        # Add buttons to Row 3, in separate columns for correct alignment
        self.layout.addWidget(self.button_createReminder, 3, 2, alignment=Qt.AlignRight)

        # Make Row 2 (the scroll area) expand vertically
        self.layout.setRowStretch(2, 1) 
        
        # Make Column 1 (the middle) expand horizontally, pushing buttons apart
        self.layout.setColumnStretch(1, 1)

        self.setLayout(self.layout)

    def reminder_clicked_handler(self, reminder_id):
        self.reminder_selected_signal.emit(reminder_id)


    def update_reminder_list(self, reminders_list):

        while self.reminders_layout.count():
            child = self.reminders_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        for reminder in reminders_list:
            time =  reminder.time.strftime("%H:%M")
            text = f"ID: {reminder.id} <b> {reminder.name} </b> <br>Remind at: {reminder.address}, {time}, on {reminder.date}"

            new_widget = ReminderWidget(reminder.id, text)
            new_widget.clicked_signal.connect(self.reminder_clicked_handler)

            self.reminders_layout.addWidget(new_widget)

    
        



