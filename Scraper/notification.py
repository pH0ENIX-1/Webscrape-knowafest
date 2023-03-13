import json
from winotify import Notification, audio

class Notify:
    
    def __init__(self):
        self.app_name = "Hackfest Scraper"
    
    def send_notification(self, message):
        
        notifier = Notification(
            app_id="Web-scraper",
            title="New Event",
            msg=message,
            icon="C:\\Users\\sanja\\Documents\\GitHub\\Webscrape-knowafest\\notification_icon.png"

        )
        notifier.set_audio(audio.Mail,loop=False)

        notifier.add_actions(label="Take Me", launch="https://www.knowafest.com/explore/category/Hackathon")
        notifier.show()
        

