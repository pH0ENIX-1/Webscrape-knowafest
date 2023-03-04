from bs4 import BeautifulSoup
import requests

# html_file = requests.get('https://www.knowafest.com/explore/category/Hackathon').text
# print(html_file)
# with open('site.html','w') as website:
    # website.write(html_file)

with open('site.html','r') as website:
    soup = BeautifulSoup(website,'lxml')
    hackathons = soup.find_all('tr')
    with open('hackathons.txt','a') as outfile:

        for hackathon in hackathons:
            hackathon = hackathon.text
            outfile.write(hackathon)
            print(hackathon.split('\n'))




