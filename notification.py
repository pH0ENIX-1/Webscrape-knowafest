from plyer import notification
import time

class Notify:
    
    def __init__(self):
        self.title = "Hackfest Scraper"
    
    def send_notification(self, message):
        notification.notify(
            title = self.title,
            message = message
        )



notification_manager = Notify()
notification_manager.send_notification("hello world")