from bs4 import BeautifulSoup
import requests
import pandas as pd
import json

class Scraper:
    
    def __init__(self, text_filename :str = "hackathons.txt", xlsx_filename :str = "hackathon_data.xlsx"):
        
        setting_handler = open("settings.json")
        settings = json.load(setting_handler)
        
        self.file_name = settings["text"]
        self.xlsx_name = settings["xlsx"]
        self.html_name = settings["html"]
        self.url = settings["url"]

    def request_site(self):
        
        html_file = requests.get(self.url).text
        with open(self.html_name,'w') as website:
            website.write(html_file)

    def preprocess_data(self, row_data:str):
        
        row_data = row_data.split('\n')
        row_data.pop(4)
        
        for element in row_data:
            if element == '':
                row_data.remove(element)
        
        return row_data

    def write_data(self):   
        
        with open(self.html_name,'r') as website:
            
            soup = BeautifulSoup(website,'lxml')
            hackathons = soup.find_all('tr')
            locations = soup.find_all("span", itemprop = "name")
            register_links = soup.find_all("tr", itemtype="http://schema.org/Event")
            print(register_links[0].get("onClick"))
            
            with open(self.file_name,'w') as outfile:
                
                dataframe_columns = hackathons.pop(0).text.split("\n")
                dataframe_columns.pop(4)
                self.hack_data = pd.DataFrame(columns = dataframe_columns)
                
                for index in range(len(hackathons)):
                    
                    hackathon = hackathons[index].text
                    location = locations[index].text
                    
                    outfile.write(hackathon)

                    row_data = self.preprocess_data(hackathon)
                    row_data.append(location)

                    self.hack_data.loc[len(self.hack_data.index)] = row_data
                
                print(self.hack_data)
                self.hack_data.to_excel(self.xlsx_name)

    def scrape_data(self):
        
        # self.request_site()
        self.write_data()


scraper_object = Scraper()
scraper_object.scrape_data()
