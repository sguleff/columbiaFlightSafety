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
    data['Origin'] = 'KEWR' 
    data['Destination'] = 'ZBAA'
    data['Departure'] = '10/1/2016 12:10pm' 
    data['Arrival'] = '10/2/2016 12:10pm'
    data['DurationMin'] = 433 
    data['ZuluTime'] = '0745Z'
    data['DistancePlanned'] = 7016
    data['DistanceFlown'] = 7279
    data['DirectDistance'] = 6822
    data['Route'] = 'GAYEL Q812 SYR TULEG YYB 5000N/08500W 5300N/09000W 5700N/09500W BINLO DUKPA 6900N/12000W SIKBU 7200N/14100W PILUN B969 BELEK B969 RODOK G495 KU G496 NAREM B161 SULOK Y327 POLHO G218 TMR B458 TZH A596 KM'
    retlist.append(data)
    return retlist

def simulateGetFlightTrackLog(date = '19010101', FlightNumber = 'UA88', ZuluTime = '1245Z', DepartureAirportCode = 'DDDD', ArrivalAirportCode = 'AAAA'):
    retlist = []
    data = {}

    data['UniversalTime'] = '19010101'
    data['Latitude'] = 11.22
    data['Longitude'] = -145.22 
    data['Course'] = 123
    data['Direction'] = 'NorthEast'
    data['KTS'] = 543
    data['MPH'] = 433 
    data['Elevation'] = 35000
    data['AscRate'] = 1200
    data['ReportingFacility'] = 'Boston Center'
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
    try:
        flighthistory = []
        next = True
        
        #first availible history:
        aircraft = ""
        date = ""
        origin = ""
        destination = "" 
        arriavl = ""
        departure = ""
        duration = ""
        zulutime = ""
        distance_planned = ""
        distance_flown = ""
        distance_direct = ""
        route = ""

        linkinfo = []
        #get the parts to form link:
        url = "http://flightaware.com/live/flight/"+FlightNumber+"/history"
        r = urllib.urlopen(url).read()
        soup = BeautifulSoup(r,"lxml")
        table = soup.find("table",{"class":"prettyTable fullWidth tablesaw tablesaw-stack"})
        aircraft = str(table.find_all("tr")[2].find_all("td")[1].text)
        link = [x['href'] for x in table.find_all("a")]
        link = [x for x in link if "history" in x]
        link = [x.split("/")[-3:] for x in link]
        k = sorted(link)
        linkinfo = [k[i] for i in range(len(k)) if i == 0 or k[i] != k[i-1]]
        #set startingdate
        date = 20161003
        
        next = True
        #number of possible links:
        while next:
            #try if any route works
            for n in linkinfo:
                data = {}
                date = str(date)
                zulutime = n[0]
                origin = n[1]
                destination = n[2]
                url = "http://flightaware.com/live/flight/"+FlightNumber+"/history/"+str(date)+"/"+zulutime+"/"+origin+"/"+destination
                r = urllib.urlopen(url).read()
                soup = BeautifulSoup(r,"lxml")

                #check if combination exist:
                tables = soup.find_all("table") 
                if len(tables) != 8:
                    continue
                #if len(tables) == 8:
                else:
                    table1 = soup.find("table",{"class":"track-panel-course"})
                    l = table1.find_all("tr")[1].find_all("td")

                    #DEPARTURE
                    departure = l[0].text.encode('utf-8').strip('\n')[0:7]
                    departure = datetime.strptime(str(date + departure),"%Y%m%d%I:%M%p")
                    
                    #ARRIVAL
                    arrival = l[1].text.encode('utf-8').strip('\n').replace('\xc2\xa0', '')
                    if '(+1)' in arrival:
                        arrival = datetime.strptime(str(date + arrival[0:7]),"%Y%m%d%I:%M%p") + timedelta(days=1)
                    else:
                        arrival = datetime.strptime(str(date + arrival[0:7]),"%Y%m%d%I:%M%p")
                    
                    #DURATION
                    duration = soup.find("div",{"class":"track-panel-duration"}).text.split(":")[1].strip()
                    duration = duration.encode('utf-8').split(" ")
                    hour = 0
                    if len(duration)> 2:
                        hour = int(duration[0])
                        duration = 60*hour + int(duration[2])
                    else:
                        duration = int(duration[0])
                    
                    #DISTANCE AND ROUTE
                    table2 = soup.find("table",{"class":"layout-table track-panel-data"})
                    for row in table2.find_all("tr"):
                        if row.find("th").text == "Distance":
                            distance = row.find("td").text.encode('utf-8').strip('\n').split("sm")
                            distance_direct = distance[0].split(":")[1].replace(",","")
                            distance_planned = distance[1].split(":")[1].replace(",","")
                            if len(distance) > 3:
                                distance_flown = distance[2].split(":")[1].replace(",","")
                        elif row.find("th").text == "Route":
                            route = row.find("td").text.encode('utf-8')
                        
                        #output data:
                    data['FlightDate'] = str(date)
                    data['FlightNumber'] = str(FlightNumber)
                    data['AircraftType'] = str(aircraft)
                    data['Origin'] = str(origin)
                    data['Destination'] = str(destination)
                    data['Departure'] = str(departure.strftime("%Y-%m-%d %I:%M %p"))
                    data['Arrival'] = str(arrival.strftime("%Y-%m-%d %I:%M %p"))
                    data['DurationMin'] = int(duration) 
                    data['ZuluTime'] = str(zulutime)
                    data['DistancePlanned'] = int(distance_planned)
                    data['DistanceFlown'] = int(distance_flown)
                    data['DirectDistance'] = int(distance_direct)
                    data['Route'] = str(route)
                    
                    flighthistory.append(data)
               
            date_format = datetime.strptime(str(date),"%Y%m%d")
            yesterday = date_format - timedelta(days=1)
            date = yesterday.strftime("%Y%m%d")
            #set end period:
            if int(date) < 20160900:
                next = False  

        return  flighthistory
    except:
        return  None

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
    soup = BeautifulSoup(r, "lxml")
    table = soup.find("table", {"id":"tracklogTable"})

    #sometimes we will not get flight details
    if table == None:
        return None

    data = []
    rows = table.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        timestamp = re.findall(r'<td align="left"><span class="show-for-medium-up-table">(.+)</span><span class="hide-for-medium-up">.+</span></td>', str(cols[0]))[0]
        latitude = re.findall(r'<td align="right"><span class="show-for-medium-up-table">(-*\d+.\d+)</span><span class="hide-for-medium-up">-*\d+\.\d+</span></td>', str(cols[1]))[0]
        longitude = re.findall(r'<td align="right"><span class="show-for-medium-up-table">(-*\d+.\d+)</span><span class="hide-for-medium-up">-*\d+\.\d+</span></td>', str(cols[2]))[0]
        course = re.findall(r'\d+', str(cols[3]))[0]
        direction = re.findall(r'<td align="left"><span class="show-for-medium-up-table">(\w+)</span>', str(cols[4]))[0]
        KTS = re.findall(r'<td align="right">(\d+)</td>', str(cols[5]))[0]
        MPH = re.findall(r'(\d+)', str(cols[6]))[0]
        feet = re.findall(r'(\d+,*\d+)', str(cols[7]))[0]
        rate = None
        reporting_facility = re.findall(r'<td align="left" class="show-for-large-up-table"><img height="12" src="https://flightaware.com/images/live/center.gif" width="12"/> (\w+.+)</td>', str(cols[9]))
        cols = [timestamp, latitude, longitude, course, direction, KTS, MPH, feet, rate, reporting_facility]
        if len(cols) == 10:
            data.append([ele for ele in cols]) # append all values (even None)
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