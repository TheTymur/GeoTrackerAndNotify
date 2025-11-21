from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QIcon

class PermissionRequest():
    def show_requestbox(self, msg):
        self.box = QMessageBox()
        self.box.setWindowTitle("Permission request")
        self.box.setWindowIcon(QIcon(r"./assets/Icons/permission.png"))
        self.box.setText(msg)
        self.box.setIcon(QMessageBox.Question)
        self.box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        self.box.setDefaultButton(QMessageBox.No)

        reply = self.box.exec_() 
      
        return reply == QMessageBox.Yes