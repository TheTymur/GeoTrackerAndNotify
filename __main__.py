from GUI import MyGeoTrackerUI, setup_Reminder_screen
from Event_manager import Event_manager
from PyQt5.QtWidgets import QApplication
from Event_manager import run_server
import threading
import sys


if __name__ == "__main__":

    flask_thread = threading.Thread(target=run_server, daemon=True)
    flask_thread.start()

    app = QApplication(sys.argv)
    main_window = MyGeoTrackerUI()

    manager = Event_manager(main_window)   
    manager.create_reminder_signal_connection(main_window)
    manager.location_updated.connect(main_window.set_location)

    main_window.show()
    sys.exit(app.exec_())