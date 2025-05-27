from bs4 import BeautifulSoup
import requests

url = "https://www.espn.com/racing/standings"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

page = requests.get(url, headers=headers)

soup = BeautifulSoup(page.text, "html.parser")

table = soup.find('table')

names = []
points = []

row = table.find('td', class_='sortcell')
name = row.find_next('td')
names.append(name)
point = name.find_next('td')
points.append(point)
row = row.find_next('td', class_='sortcell')

while row != None:
    name = row.find_next('td')
    names.append(name)
    point = name.find_next('td')
    points.append(point)
    row = row.find_next('td', class_='sortcell')

for i in range(len(names)):
    print(names[i].text, points[i].text)