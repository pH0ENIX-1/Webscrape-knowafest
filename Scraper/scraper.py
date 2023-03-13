from bs4 import BeautifulSoup
import requests
import pandas as pd
import json
import xlsxwriter

class Scraper:
    
    def __init__(self):
        
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
        
        prev_hackdata = pd.read_excel("hackathon_data.xlsx")
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
                    
                
                self.hack_data['Start Date'] = pd.to_datetime(self.hack_data['Start Date'],dayfirst=True)
                self.hack_data.to_excel("hackathon_data.xlsx")
                for index in range(1,len(self.hack_data)):
                    if self.hack_data.loc[index,'Start Date'] < pd.datetime.now():
                        self.hack_data.drop(index=index, axis=0, inplace=True)

                df_all = self.hack_data.merge(prev_hackdata.drop_duplicates(), on="Fest Name",
                   how='left', indicator=True)

                #create DataFrame with rows that exist in first DataFrame only
                new_events = df_all[df_all['_merge'] == 'left_only']

                self.hack_data.to_excel(self.xlsx_name)

                if not new_events.empty:
                    print("new Event Found!")
                    return "new Event"
                else:
                    print("No new events found.")

    def scrape_data(self):
        
        # self.request_site()
        return self.write_data()


# scraper_object = Scraper()
# scraper_object.scrape_data()
# print(scraper_object.hack_data.info())
