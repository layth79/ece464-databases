# ECE-464 Assignment 2: webscraper code
# Layth Yassin 
# Professor Sokolov

from bs4 import BeautifulSoup
import pymongo
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

# connect to mongoDB
client = pymongo.MongoClient("mongodb+srv://m001-student:m001-mongodb-basics@sandbox.p6etn.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client.nbaStats

# initialize web driver
s = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=s)
driver.maximize_window()

# navigate to nba website
url = "https://www.nba.com/stats/alltime-leaders/"
driver.get(url)

# list that will store all the player dicts
players = []

# f = open("out.txt", "w")
# loop through 27 pages to get all-time leaders' stats
for i in range(0, 27):
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("div", class_="nba-stat-table__overflow")

    for row in table.findAll("tr"):
        element = row.td
        if element:
            nextSiblings = element.find_next_siblings("td")
            player = {}

            # insert the data into player dict
            player['name'] = nextSiblings[0].text.strip() if nextSiblings[0].text.strip() != '-' else None
            player['gp'] = int(nextSiblings[1].text.strip().replace(',', '')) if nextSiblings[1].text.strip().replace(',', '') != '-' else None
            player['min'] = int(nextSiblings[2].text.strip()) if nextSiblings[2].text.strip() != '-' else None
            player['pts'] = int(nextSiblings[3].text.strip()) if nextSiblings[3].text.strip() != '-' else None
            player['fgm'] = int(nextSiblings[4].text.strip()) if nextSiblings[4].text.strip() != '-' else None
            player['fga'] = int(nextSiblings[5].text.strip()) if nextSiblings[5].text.strip() != '-' else None
            player['fg%'] = float(nextSiblings[6].text.strip()) if nextSiblings[6].text.strip() != '-' else None
            player['3pm'] = int(nextSiblings[7].text.strip()) if nextSiblings[7].text.strip() != '-' else None
            player['3pa'] = int(nextSiblings[8].text.strip()) if nextSiblings[8].text.strip() != '-' else None
            player['3p%'] = float(nextSiblings[9].text.strip()) if nextSiblings[9].text.strip() != '-' else None
            player['ftm'] = int(nextSiblings[10].text.strip()) if nextSiblings[10].text.strip() != '-' else None
            player['fta'] = int(nextSiblings[11].text.strip()) if nextSiblings[11].text.strip() != '-' else None
            player['ft%'] = float(nextSiblings[12].text.strip()) if nextSiblings[12].text.strip() != '-' else None
            player['oreb'] = int(nextSiblings[13].text.strip()) if nextSiblings[13].text.strip() != '-' else None
            player['dreb'] = int(nextSiblings[14].text.strip()) if nextSiblings[14].text.strip() != '-' else None
            player['reb'] = int(nextSiblings[15].text.strip()) if nextSiblings[15].text.strip() != '-' else None
            player['ast'] = int(nextSiblings[16].text.strip()) if nextSiblings[16].text.strip() != '-' else None
            player['stl'] = int(nextSiblings[17].text.strip()) if nextSiblings[17].text.strip() != '-' else None
            player['blk'] = int(nextSiblings[18].text.strip()) if nextSiblings[18].text.strip() != '-' else None
            player['tov'] = int(nextSiblings[19].text.strip()) if nextSiblings[19].text.strip() != '-' else None
            player['efg%'] = float(nextSiblings[20].text.strip()) if nextSiblings[20].text.strip() != '-' else None
            player['ts%'] = float(nextSiblings[21].text.strip()) if nextSiblings[21].text.strip() != '-' else None
            
            # append player dict to players list
            players.append(player)

            # f.write(str(player))
            # f.write('\n')      

    # click button to go to next page
    time.sleep(1)
    try:
        driver.find_element(By.CLASS_NAME, "stats-table-pagination__next").click()
    except:
        continue
    time.sleep(1)

# insert player documents into mongoDB database
try:
    db.playerStats.insert_many(players)
except:
    print("ERROR: data was not inserted into database")

# f.close()
driver.quit()
