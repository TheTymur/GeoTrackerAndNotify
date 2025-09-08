import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Signals & Slots")

        # Widgets
        self.label = QLabel("Press the button")
        self.button = QPushButton("Click Me!")

        # Connect button click to a function
        self.button.clicked.connect(self.on_button_click)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.button)
        self.setLayout(layout)

    def on_button_click(self):
        if self.label.text() == "Press the button":
            self.label.setText("It was clicked for first time!")
        else:
            self.label.setText("Button was clicked!")

app = QApplication(sys.argv)
screen = MyWindow()
screen.show()
sys.exit(app.exec_())
