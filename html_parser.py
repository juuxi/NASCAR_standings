from bs4 import BeautifulSoup
import requests
import csv

url_standings = "https://www.espn.com/racing/standings"

url_team_driver = "https://en.wikipedia.org/wiki/2025_NASCAR_Cup_Series"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

page = requests.get(url_standings, headers=headers)

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
    names[i] = names[i].text
    points[i] = points[i].text

names[names.index("AJ Allmendinger")] = "A. J. Allmendinger"

with open('scoreboard.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    to_write = [list(pair) for pair in zip(names, points)]
    writer.writerows(to_write)


page = requests.get(url_team_driver, headers=headers)

soup = BeautifulSoup(page.text, "html.parser")

table = soup.find('table')

teams = [None] * len(names)

team = table.find('td')

while team:
    if team.text.__contains__("["):
        team.string = team.text[:-9]

    number = team.find_next('td')
    if team.has_attr('rowspan'):
        for i in range(int(team['rowspan'])):
            while not number.text[0].isdigit():
                number = number.find_next('td')

            driver = number.find_next('td')

            if driver.text.__contains__("(R)"):
                driver.string = driver.text[:-4]
            if driver.text.__contains__("Daniel"):
                driver.string = "Daniel Suarez\n"
            if driver.text.__contains__("Alfredo") or driver.text.__contains__("McLeod") or driver.text.__contains__("Yeley") or driver.text.__contains__("Hill") or driver.text.__contains__("Zilisch"):
                continue
            if driver.text.__contains__("Chandler Smith"):
                continue   

            teams[names.index(driver.text[:-1])] = team.text[:-1]

            number = number.find_next('td')

    else:
        driver = number.find_next('td')
        if driver.text.__contains__("Allgaier") or driver.text.__contains__("Brown") or driver.text.__contains__("Heim"):
            team = team.find_next('td', {"style" : "text-align:center;"})
            continue
        teams[names.index(driver.text[:-1])] = team.text[:-1]

    team = team.find_next('td', {"style" : "text-align:center;"})

with open('team-driver.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    to_write = [list(pair) for pair in zip(names, teams)]
    writer.writerows(to_write)
