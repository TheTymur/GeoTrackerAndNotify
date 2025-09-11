from GUI import MyGeoTrackerUI


__all__ = ["Event_manager"]
class Event_manager:
    def update_location(self, window: MyGeoTrackerUI):
        window.set_location("Poland")
 
    def conect_signals(self, window: MyGeoTrackerUI):
        window.button_findme.clicked.connect(lambda: self.update_location(window))

