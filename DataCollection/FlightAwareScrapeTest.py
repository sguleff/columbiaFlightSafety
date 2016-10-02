from bs4 import BeautifulSoup
import urllib

#sample code here
'''url = 'https://flightaware.com/live/flight/UAL88/history/20160924/0745Z/ZBAA/KEWR/tracklog'

r = urllib.urlopen(url).read()
soup = BeautifulSoup(r)

table = soup.find("table", {"id":"tracklogTable"})

data = []

rows = table.find_all('tr')

for row in rows:
    cols = row.find_all('td')
    cols = [ele.text.strip() for ele in cols]
    if len(cols) == 10:
        data.append([ele for ele in cols if ele]) # Get rid of empty values'''


def getAvailableFlightHistory(FlightNumber):
    '''Returns a list of dictionaries containing flights available to scrape:
       Dictionary entities available:
           departure date as '20160924'
           Flight number as 'UA88'
           ZuluTime as '0745Z'
           DepartureAirportCode as 'ZBAA'
           ArrivalAirportCode as 'KEWR'
       '''
    url = 'https://flightaware.com/live/flight/' + FlightNumber
    r = urllib.urlopen(url).read()
    soup = BeautifulSoup(r)
    data = []
    rowodd = soup.find_all("tr", class_="smallActiverow1")
    roweven = soup.find_all("tr", class_="smallActiverow2")
    for row in rowodd:
        lstFlight = row.find('a')['href'].split('/')
        if len(lstFlight) == 9:
            data.append({'FlightNumber':lstFlight[3], 'date':lstFlight[5], 'ZuluTime':lstFlight[6], 'DepartureAirportCode': lstFlight[7], 'ArrivalAirportCode': lstFlight[8]})
    for row in roweven:
        lstFlight = row.find('a')['href'].split('/')
        if len(lstFlight) == 9:
            data.append({'FlightNumber':lstFlight[3], 'date':lstFlight[5], 'ZuluTime':lstFlight[6], 'DepartureAirportCode': lstFlight[7], 'ArrivalAirportCode': lstFlight[8]})
    return data

def getFlightTrackLog2(flightInfoDict = {}):
    '''scrape a flight track log from a flight given a dictionary containing:
       departure date as '20160924'
       Flight number as 'UA88'
       ZuluTime as '0745Z'
       DepartureAirportCode as 'ZBAA'
       ArrivalAirportCode as 'KEWR'
       '''
    date = flightInfoDict['date']
    FlightNumber = flightInfoDict['FlightNumber']
    ZuluTime = flightInfoDict['ZuluTime']
    DepartureAirportCode = flightInfoDict['DepartureAirportCode']
    ArrivalAirportCode = flightInfoDict['ArrivalAirportCode']
    return getFlightTrackLog(date = date, FlightNumber = FlightNumber, ZuluTime =  ZuluTime, DepartureAirportCode = DepartureAirportCode, ArrivalAirportCode = ArrivalAirportCode)

def getFlightTrackLog(date = '', FlightNumber = '', ZuluTime = '', DepartureAirportCode = '', ArrivalAirportCode = ''):
    '''scrape a flight track log from a flight given:
       departure date as '20160924'
       Flight number as 'UA88'
       ZuluTime as '0745Z'
       DepartureAirportCode as 'ZBAA'
       ArrivalAirportCode as 'KEWR'
       '''
    url = 'https://flightaware.com/live/flight/' + FlightNumber + '/history/'+ date +'/' + ZuluTime +'/'+ DepartureAirportCode +'/'+ ArrivalAirportCode+ '/tracklog'
    r = urllib.urlopen(url).read()
    soup = BeautifulSoup(r)

    table = soup.find("table", {"id":"tracklogTable"})

    #sometimes we will not get flight details
    if table == None:
        return None

    data = []

    rows = table.find_all('tr')

    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        if len(cols) == 10:
            data.append([ele for ele in cols if ele]) # Get rid of empty values

    return data

def getAllDepartingFlights(AirportCode = '', number = 1000):
    '''Scrape all flight departing from a specified airport:
    AirportCode as 'KDEN'
    '''
    getMoreFlights = True
    i = 0
    
    data = {}

    while getMoreFlights:
        url = 'http://flightaware.com/live/airport/'+AirportCode +'/departures?;offset='+ str(i)+';order=actualarrivaltime;sort=DESC'
        r = urllib.urlopen(url).read()
        soup = BeautifulSoup(r)
        table = soup.find("table", class_="prettyTable")

        rows = table.find_all("tr")

        for row in rows:
            if len(row.find_all('td')) == 6:
                cols = row.find_all('td')
                if not data.has_key(cols[0]):
                    data[cols[0].text.encode("utf8").strip()] = False
        i += 20
        if number / i < 1:
            break
    return data

def getAllArrivingFlights(AirportCode = '', number = 1000):
    '''Scrape all flight departing from a specified airport:
    AirportCode as 'KDEN'
    '''
    getMoreFlights = True
    i = 0
    
    data = {}

    while getMoreFlights:
        url = 'http://flightaware.com/live/airport/'+AirportCode +'/arrivals?;offset='+ str(i)+';order=actualarrivaltime;sort=DESC'
        r = urllib.urlopen(url).read()
        soup = BeautifulSoup(r)
        table = soup.find("table", class_="prettyTable")

        rows = table.find_all("tr")

        for row in rows:
            if len(row.find_all('td')) == 5:
                cols = row.find_all('td')
                if not data.has_key(cols[0]):
                    data[cols[0].text.encode("utf8").strip()] = False
        i += 20
        if number / i < 1:
            break
    return data


#we should never run this module
def main():
    pass

if __name__ == "__main__":
    main()