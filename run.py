from GUI import MyGeoTrackerUI
from Event_manager import EventManager
from PyQt5.QtWidgets import QApplication
from Event_manager import run_server, NotificationLogic
import threading
import sys


if __name__ == "__main__":

    flask_thread = threading.Thread(target=run_server, daemon=True)
    flask_thread.start()

    app = QApplication(sys.argv)
    main_window = MyGeoTrackerUI()

    notification = NotificationLogic(main_window)
    notification.connect_signals()

    manager = EventManager(main_window)   
    manager.create_reminder_signal_connection(main_window)
    manager.location_updated.connect(main_window.set_location)

    main_window.show()

    sys.exit(app.exec_())