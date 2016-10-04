from bs4 import BeautifulSoup
import urllib
import requests

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



def simulateGetAvailableFlightHistory():
    retlist = []
    data = {}
    data['FlightDate'] = '20160930'
    data['FlightNumber'] = 'UAL88'
    data['AircraftType'] = 'B772'
    data['Origin'] = 'ZBAA' 
    data['Destination'] = 'KEWR'
    data['Departure'] = '10/1/2016 12:10pm' 
    data['Arrival'] = '10/2/2016 12:10pm'
    data['DurationMin'] = 433 
    data['ZuluTime'] = '1555Z'
    data['DistancePlanned'] = 7016
    data['DistanceFlown'] = 7279
    data['DirectDistance'] = 6822
    data['Route'] = 'GAYEL Q812 SYR TULEG YYB 5000N/08500W 5300N/09000W 5700N/09500W BINLO DUKPA 6900N/12000W SIKBU 7200N/14100W PILUN B969 BELEK B969 RODOK G495 KU G496 NAREM B161 SULOK Y327 POLHO G218 TMR B458 TZH A596 KM'
    retlist.append(data)
    return retlist




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
            data.append({'FlightNumber':lstFlight[3], 'flightdate':lstFlight[5], 'ZuluTime':lstFlight[6], 'DepartureAirportCode': lstFlight[7], 'ArrivalAirportCode': lstFlight[8]})
    for row in roweven:
        lstFlight = row.find('a')['href'].split('/')
        if len(lstFlight) == 9:
            data.append({'FlightNumber':lstFlight[3], 'flight':lstFlight[5], 'ZuluTime':lstFlight[6], 'DepartureAirportCode': lstFlight[7], 'ArrivalAirportCode': lstFlight[8]})
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

def getAllArrivingFlights(airportCode):
    '''returns list of all Arriving flights from a specified airportCode'''
    try:
        arrival = []
        n = 0
        page = True
        while page is True:
            url = "http://flightaware.com/live/airport/"+airportCode+"/arrivals?;offset="+str(20*n)+";order=actualarrivaltime;sort=DESC"
            soup = BeautifulSoup(requests.get(url).content,"html.parser")
            table = soup.find("table",{"class":"prettyTable fullWidth"})
            for row in table.find_all('tr')[2:]:
                flight = row.find_all("td")[0].text
                if "Sorry" in flight:
                    page = False
                else:
                    arrival.append(flight)
            n +=1
        return set(arrival)
    except:
        return None

def getAllDepartingFlights(airportCode):
    '''returns list of all Departing flights from a specified airportCode'''
    try:
        arrival = []
        n = 0
        page = True
        while page is True:
            url = "http://flightaware.com/live/airport/"+airportCode+"/departures?;offset="+str(20*n)+";order=actualarrivaltime;sort=DESC"
            soup = BeautifulSoup(requests.get(url).content,"html.parser")
            table = soup.find("table",{"class":"prettyTable fullWidth"})
            for row in table.find_all('tr')[2:]:
                flight = row.find_all("td")[0].text
                if "Sorry" in flight:
                    page = False
                else:
                    arrival.append(flight)
            n +=1
        return set(arrival)
    except:
        return None


#we should never run this module
def main():
    pass

if __name__ == "__main__":
    main()