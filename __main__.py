from GUI import MyGeoTrackerUI
from Event_manager import Event_manager
from PyQt5.QtWidgets import QApplication
from Event_manager import run_server
import threading
import sys


if __name__ == "__main__":

    flask_thread = threading.Thread(target=run_server, daemon=True)
    flask_thread.start()

    app = QApplication(sys.argv)
    window = MyGeoTrackerUI()

    manager = Event_manager()   
    manager.conect_signals(window)

    window.show()
    sys.exit(app.exec_())