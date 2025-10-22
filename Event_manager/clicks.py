from GUI import MyGeoTrackerUI
from . import location_getter_api

__all__ = ["Event_manager"]


class Event_manager:
    def __init__(self):
        self.clicked = 0

    def update_location(self, window: MyGeoTrackerUI):
        current_address = location_getter_api.address
        if self.clicked:
            if current_address:
                window.set_location(current_address)
                self.clicked = 0
            else:
                window.set_location("Unknown")
                self.clicked = 0
        else: 
            window.set_location("Krakow")
            self.clicked = 1

 
    def conect_signals(self, window: MyGeoTrackerUI):
        window.button_findme.clicked.connect(lambda: self.update_location(window))


