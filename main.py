from bs4 import BeautifulSoup
import requests
import pandas as pd

# html_file = requests.get('https://www.knowafest.com/explore/category/Hackathon').text
# print(html_file)
# with open('site.html','w') as website:
    # website.write(html_file)

def preprocess_data(row_data:str):
    row_data = row_data.split('\n')
    row_data.pop(4)
    for element in row_data:
        if element == '':
            row_data.remove(element)
    return row_data

with open('site.html','r') as website:
    soup = BeautifulSoup(website,'lxml')
    hackathons = soup.find_all('tr')
    locations = soup.find_all("span", itemprop = "name")
    
    with open('hackathons.txt','w') as outfile:
        dataframe_columns = hackathons.pop(0).text.split("\n")
        dataframe_columns.pop(4)
        print(dataframe_columns)
        hack_data = pd.DataFrame(columns = dataframe_columns)
        for index in range(len(hackathons)):
            
            hackathon = hackathons[index].text
            location = locations[index].text
            
            outfile.write(hackathon)

            row_data = preprocess_data(hackathon)
            row_data.append(location)
            print(row_data)

            hack_data.loc[len(hack_data.index)] = row_data
        
        print(hack_data)
        hack_data.to_excel("hackathon_data.xlsx")


