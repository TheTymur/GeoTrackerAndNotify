from GUI import MyGeoTrackerUI
from Event_manager import Event_manager
from PyQt5.QtWidgets import QApplication
import sys


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyGeoTrackerUI()

    manager = Event_manager()   
    manager.conect_signals(window)

    window.show()
    sys.exit(app.exec_())