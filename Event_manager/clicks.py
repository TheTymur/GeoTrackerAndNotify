from GUI import MyGeoTrackerUI
from . import location_getter_api

__all__ = ["Event_manager"]

class Event_manager:
    clicked = 0
    def update_location(self, window: MyGeoTrackerUI):
        if self.clicked:
            window.set_location(location_getter_api.address)
            self.clicked = 0
        else: 
            window.set_location("Krakow")
            self.clicked = 1

 
    def conect_signals(self, window: MyGeoTrackerUI):
        window.button_findme.clicked.connect(lambda: self.update_location(window))


