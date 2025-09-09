import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QGridLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

font_header = QFont("Arial", 16, QFont.Bold)
font_simple = QFont("Arial", 12)
font_simple.setItalic(True)
class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.wrong_button = False

        self.setWindowTitle("Grid Layout Example")
        self.resize(600, 300)

        self.header = QLabel("Top Center (span 2)")
        self.instruction = QLabel("Please click 'ME!' to change text in a header.")
        self.button_ME = QPushButton("ME")
        self.button_left_bottom = QPushButton("Left bottom")
        self.button_right_bottom = QPushButton("Right bottom")
        self.layout = QGridLayout()

        self.layout.addWidget(self.header, 0, 0, 1, 3, alignment=Qt.AlignCenter);    self.header.setFont(font_header)
        self.layout.addWidget(self.instruction, 1, 1, alignment=Qt.AlignCenter); self.instruction.setFont(font_simple)
        self.layout.addWidget(self.button_left_bottom, 1, 0)
        self.layout.addWidget(self.button_right_bottom, 1, 2)                #shift+alt to start typing
        self.layout.addWidget(self.button_ME, 2, 0, 1, 3)

        self.setLayout(self.layout)
        self.header.setText("New Text! blah blah \n Some more \n Strange")
        self.header.setAlignment(Qt.AlignCenter)

        self.button_ME.clicked.connect(self.textChange)
        self.button_left_bottom.clicked.connect(self.anotherClicked)
        self.button_right_bottom.clicked.connect(self.anotherClicked)

    def textChange(self):
        if self.wrong_button:
            self.header.setText("Finally, you found the right button!")
            self.header.setAlignment(Qt.AlignCenter)
            self.wrong_button = False
        else:
            self.header.setText("You changed header... \n Is it legal?")
            self.header.setAlignment(Qt.AlignCenter)
        return self.wrong_button
        
    def anotherClicked(self):
        self.header.setText("Well, wrong button!")
        self.header.setAlignment(Qt.AlignCenter)
        self.wrong_button = True
        return self.wrong_button
    



app = QApplication(sys.argv)
window = MyWindow()
window.show()
sys.exit(app.exec_())
