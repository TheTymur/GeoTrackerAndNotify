from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QIcon

__all__ = ["ErrorNotify"]

class ErrorNotify(QObject):
    show_error_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.show_error_signal.connect(self._show_error)

    def show_error(self, msg):
        self.show_error_signal.emit(msg)
    
    def _show_error(self, msg):
        self.box = QMessageBox()
        self.box.setWindowTitle("Error")
        self.box.setWindowIcon(QIcon("C:\Python\GeoTrackerAndNotify\GUI\Icons\error.png"))
        self.box.setText(msg)
        self.box.setIcon(QMessageBox.Critical)
        self.box.setStandardButtons(QMessageBox.Ok)
        self.box.exec_() 

