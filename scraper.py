from bs4 import BeautifulSoup
import requests
import pandas as pd

class Scraper:
    
    def __init__(self, text_filename :str = "hackathons.txt", xlsx_filename :str = "hackathon_data.txt"):
        self.file_name = text_filename
        self.xlsx_name = xlsx_filename

    def request_site(self, url = "https://www.knowafest.com/explore/category/Hackathon"):
        
        html_file = requests.get(url).text
        with open('site.html','w') as website:
            website.write(html_file)

    def preprocess_data(self, row_data:str):
        
        row_data = row_data.split('\n')
        row_data.pop(4)
        for element in row_data:
            if element == '':
                row_data.remove(element)
        return row_data

    def write_data(self):   
        
        with open('site.html','r') as website:
            
            soup = BeautifulSoup(website,'lxml')
            hackathons = soup.find_all('tr')
            locations = soup.find_all("span", itemprop = "name")
            register_links = soup.find_all("tr", itemtype="http://schema.org/Event")
            print(register_links[0].get("onClick"))
            with open('hackathons.txt','w') as outfile:
                
                dataframe_columns = hackathons.pop(0).text.split("\n")
                dataframe_columns.pop(4)
                # print(dataframe_columns)
                self.hack_data = pd.DataFrame(columns = dataframe_columns)
                
                for index in range(len(hackathons)):
                    
                    hackathon = hackathons[index].text
                    location = locations[index].text
                    
                    outfile.write(hackathon)

                    row_data = self.preprocess_data(hackathon)
                    row_data.append(location)
                    # print(row_data)

                    self.hack_data.loc[len(self.hack_data.index)] = row_data
                
                print(self.hack_data)
                self.hack_data.to_excel("hackathon_data.xlsx")

    def scrape_data(self):
        
        # self.request_site()
        self.write_data()


scraper_object = Scraper()
scraper_object.scrape_data()
