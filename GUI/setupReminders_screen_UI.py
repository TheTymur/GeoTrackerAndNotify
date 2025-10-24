from PyQt5.QtWidgets import QDialog, QGridLayout, QLabel, QLineEdit, QPushButton, QSpacerItem, QSizePolicy, QHBoxLayout
from PyQt5.QtCore import Qt, QObject, pyqtSignal
from PyQt5.QtGui import QFont, QIcon, QPixmap

class setup_Reminder_screen(QDialog):
    def __init__(self):
        super().__init__()
        self._set_constants()
        self._setup_UI()

    def _set_constants(self):
        self.font_header = QFont("Arial", 16, QFont.Bold)


    def _setup_UI(self):
        self.setWindowTitle("Create reminder")
        self.resize(400,200)

        self.layout = QGridLayout()

        self.title = QLabel("Create reminder")
        self.title.setFont(self.font_header)

        self.name_reminder = QLabel("Enter reminder:")
        self.input_reminderName = QLineEdit()

        self.address = QLabel("Enter address: ")
        self.infoIcon_address = QLabel()
        self.infoIcon_address.setPixmap(QPixmap("C:\Python\GeoTrackerAndNotify\GUI\Icons\info_icon.png").scaled(16,16))
        self.infoIcon_address.setToolTip("Address where this reminder should appear, or leave blank to use your current location.")
        self.input_address = QLineEdit()

        self.date = QLabel("Enter date: ")
        self.input_date = QLineEdit()

        self.save_button = QPushButton("Save")
        self.cancel_button = QPushButton("Cancel")

        self.layout.addWidget(self.title, 0, 0, 1, 3, alignment=Qt.AlignHCenter | Qt.AlignTop)

        self.layout.addWidget(self.name_reminder, 1, 0, alignment=Qt.AlignRight)
        self.layout.addWidget(self.input_reminderName, 1, 1, 1, 2, alignment=Qt.AlignLeft)

        self.layout.addWidget(self.address, 2, 0, alignment=Qt.AlignRight)
        self.layout.addWidget(self.input_address, 2, 1, alignment=Qt.AlignLeft)
        self.layout.addWidget(self.infoIcon_address, 2, 2, alignment=Qt.AlignLeft | Qt.AlignVCenter)

        self.layout.addWidget(self.date, 3, 0, alignment= Qt.AlignRight)
        self.layout.addWidget(self.input_date, 3, 1, alignment= Qt.AlignLeft)

        self.layout.addItem(QSpacerItem(0, 40), 4, 0, 1, 3)

        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.save_button)
        buttons_layout.addSpacing(20)
        buttons_layout.addWidget(self.cancel_button)

        self.layout.addLayout(buttons_layout, 5, 0, 1, 3, alignment=Qt.AlignCenter)
        self.setLayout(self.layout)




