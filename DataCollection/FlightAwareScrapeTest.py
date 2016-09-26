from bs4 import BeautifulSoup
import urllib

url = 'https://flightaware.com/live/flight/UAL88/history/20160924/0745Z/ZBAA/KEWR/tracklog'

r = urllib.urlopen(url).read()
soup = BeautifulSoup(r)

table = soup.find("table", {"id":"tracklogTable"})

data = []

rows = table.find_all('tr')

for row in rows:
    cols = row.find_all('td')
    cols = [ele.text.strip() for ele in cols]
    if len(cols) == 10:
        data.append([ele for ele in cols if ele]) # Get rid of empty values

