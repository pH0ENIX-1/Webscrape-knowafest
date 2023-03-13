from scraper import Scraper
from notification import Notify

scraper_object = Scraper()
scraper_results = scraper_object.scrape_data()
if scraper_results == "new Event":
    notification_manager = Notify()
    notification_manager.send_notification("New Event found!")
