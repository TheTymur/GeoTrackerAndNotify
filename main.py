import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QGridLayout


class MyWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Grid Layout Example")
        self.resize(400, 200)

        self.layout = QGridLayout()

        self.layout.addWidget(QLabel("Top Center (span 2)"), 0, 1, 1, 2)
        self.layout.addWidget(QPushButton("Left Bottom"), 1, 0)
        self.layout.addWidget(QPushButton("Right Bottom"), 1, 2)                #shift+alt to start typing
        self.layout.addWidget(QPushButton("Full Width Bottom"), 2, 0, 1, 3)

        self.setLayout(self.layout)

app = QApplication(sys.argv)
window = MyWindow()
window.show()
sys.exit(app.exec_())
