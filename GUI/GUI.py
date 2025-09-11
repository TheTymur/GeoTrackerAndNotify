import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QGridLayout, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon

__all__ = ["run", "MyGeoTrackerUI", "set_location"]

class MyGeoTrackerUI(QWidget):
    def __init__(self):
        super().__init__()
        self._setup_constants()
        self._setup_UI()
        

    def set_location(self, location_txt: str):
        self.location.setText(f"location: {location_txt}")   
        
    def _setup_constants(self):
        self.font_header = QFont("Arial", 16, QFont.Bold)
        self.font_simple = QFont("Arial", 12)

    def _setup_UI(self):
        self.setWindowTitle("GeoTracker")
        self.setWindowIcon(QIcon("GeoT.png"))
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


def run():
    app = QApplication(sys.argv)
    window = MyGeoTrackerUI()
    window.show()
    sys.exit(app.exec_())
