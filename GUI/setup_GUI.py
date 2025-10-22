import sys
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QGridLayout, QSpacerItem, QSizePolicy, QMessageBox
from PyQt5.QtCore import Qt, QObject, pyqtSignal
from PyQt5.QtGui import QFont, QIcon

__all__ = ["MyGeoTrackerUI", "set_location", "ErrorHandler"]

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

    def _setup_UI(self):
        self.setWindowTitle("GeoTracker")
        self.setWindowIcon(QIcon("C:\Python\GeoTrackerAndNotify\GUI\GeoT.png"))
        self.resize(800, 800)

        self.layout = QGridLayout()
        self.title = QLabel("GeoTracker")
        self.title.setFont(self.font_header)
        self.location = QLabel("Location: Unknown")
        self.location.setFont(self.font_simple)
        self.button_findme = QPushButton("Find me")
        self.button_findme.setFixedSize(200,50)

        self.layout.addWidget(self.title, 0,0,1,3, alignment=Qt.AlignTop | Qt.AlignHCenter)
        # self.title.setContentsMargins(50, 0, 0, 0) if I wanted to make some space from the sides
        self.layout.addItem(QSpacerItem(0, 80, QSizePolicy.Minimum, QSizePolicy.Fixed), 1, 0, 1, 3)
        self.layout.addWidget(self.location, 2,0,1,3, alignment=Qt.AlignHCenter | Qt.AlignTop)
        self.layout.addItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding), 3, 0, 1, 3)
        self.layout.addWidget(self.button_findme, 4,0,1,3, alignment= Qt.AlignCenter)
        self.setLayout(self.layout)


class ErrorHandler(QObject):
    show_error_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.show_error_signal.connect(self._show_error)

    def show_error(self, msg):
        self.show_error_signal.emit(msg)
    
    def _show_error(self, msg):
        self.box = QMessageBox()
        self.box.setWindowTitle("Error")
        self.box.setWindowIcon(QIcon("C:\Python\GeoTrackerAndNotify\GUI\error.png"))
        self.box.setText(msg)
        self.box.setIcon(QMessageBox.Critical)
        self.box.setStandardButtons(QMessageBox.Ok)
        self.box.exec_() 




