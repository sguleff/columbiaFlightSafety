from bs4 import BeautifulSoup
import urllib
import requests
from datetime import datetime
from datetime import timedelta
import itertools
import re



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
                date_format = datetime.strptime(str(date),"%Y%m%d")
                zulutime = n[0]
                origin = n[1]
                destination = n[2]
                url = "http://flightaware.com/live/flight/"+FlightNumber+"/history/"+str(date)+"/"+zulutime+"/"+origin+"/"+destination
                r = urllib.urlopen(url).read()
                soup = BeautifulSoup(r,"lxml")
                #check if combination exist:
                tables = soup.find_all("table") 
                if len(tables) != 8 :
                    continue
                #if len(tables) == 8:
                else:
                    table1 = soup.find("table",{"class":"track-panel-course"})
                    l = table1.find_all("tr")[1].find_all("td")

                    #DEPARTURE
                    departure = l[0].text.encode('utf-8').strip('\n').strip(" ").replace('\xc2\xa0', '')
                    if "Cancelled" in departure:
                        continue
                    dezone =  departure[7:10]
                    #print dezone
                    #print datetime.strptime(str(date + departure[0:7]+" "+departure[7:10]),"%Y%m%d%I:%M%p %Z")
                    departure = datetime.strptime(str(date + departure[0:7]),"%Y%m%d%I:%M%p")
                    #departure = str(date_format) + departure
                    #print departure
                    
                    #ARRIVAL
                    arrival = l[1].text.encode('utf-8').strip('\n').replace('\xc2\xa0', '')
                    azone = arrival[7:10]
                    if '(+1)' in arrival:
                        arrival = datetime.strptime(str(date + arrival[0:7]),"%Y%m%d%I:%M%p") + timedelta(days=1)
                        #arrival = str(date_format + timedelta(days=1)) + arrival
                    else:
                        arrival = datetime.strptime(str(date + arrival[0:7]),"%Y%m%d%I:%M%p")
                        #arrival = str(date_format)+ arrival
                    
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
                    data['Departure'] = str(departure.strftime("%B %d %H:%M:%S %Y")) + " "+dezone
                    data['Arrival'] = str(arrival.strftime("%B %d %H:%M:%S %Y")) +" "+azone
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
            if int(date) < 20160910:
                next = False  

        return  flighthistory
    except:
        return  None


def getFlightTrackLog(date='', FlightNumber='', ZuluTime='', DepartureAirportCode='', ArrivalAirportCode=''):
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

    # sometimes we will not get flight details
    if table is None:
        return None


    retlist = []

    rows = table.find_all('tr')

    print "\nNow fetching data for: " + url

    time_location = re.search(r'class="show-for-medium-up">Time \((\w*)\)</span>', str(rows[0])).group(1)

    for row in rows:
        cols = row.find_all('td')

        if len(cols) > 7:
            data = {}
            timestamp = re.findall(r'<td align="left"><span class="show-for-medium-up-table">(.+)</span><span class="hide-for-medium-up">.+</span></td>', str(cols[0]))[0] + ' ' + time_location
            latitude = re.findall(r'<td align="right"><span class="show-for-medium-up-table">(-*\d+.\d+)</span><span class="hide-for-medium-up">-*\d+\.\d+</span></td>', str(cols[1]))[0]
            longitude = re.findall(r'<td align="right"><span class="show-for-medium-up-table">(-*\d+.\d+)</span><span class="hide-for-medium-up">-*\d+\.\d+</span></td>', str(cols[2]))[0]
            course = re.findall(r'\d+', str(cols[3]))[0]
            direction = re.findall(r'<td align="left"><span class="show-for-medium-up-table">(\w+)</span>', str(cols[4]))[0]
            KTS = re.findall(r'<td align="right">(\d*)</td>', str(cols[5]))[0]
            MPH = re.findall(r'">(\d*).*', str(cols[6]))[0]
            feet = re.findall(r'table">(\d*,*\d*)', str(cols[7]))[0]






            rate = ' '.join(list(re.findall(r'<td align="right" class="show-for-medium-up-table">(-*\d*,*\d*).*<img alt="(\w*)".+', str(cols[8]))[0])).replace(',', '')
            my_string = str(cols[9])
            reporting_facility = my_string[my_string.find('width="12"/> ') + len('width="12"/> '):my_string.find('</td>')]

            data['fTimeStamp'] = date + ' ' + timestamp
            data['latitude'] = float(latitude.replace(',',''))
            data['longitude'] = float(longitude.replace(',',''))
            data['course'] = int(course)
            data['direction'] = direction
            data['kts'] = int(KTS) if KTS != '' else None
            data['mph'] = int(MPH.replace(',','')) if MPH != '' else None
            data['elevation'] = int(feet.replace(',','')) if feet != '' else None
            data['ascrate'] = 0 if (rate == ' Level') or (rate == ' Climbing') or (rate == ' Descending') else int(rate.split()[0])

            if '</a>' in reporting_facility:
                rep_fac_temp = ''.join(list(re.findall(r'<.*>(.*)</a> (.*)', reporting_facility)[0]))
                rep_fac = rep_fac_temp.strip() if rep_fac_temp.endswith(' ') else rep_fac_temp
                data['reportingfacility'] = rep_fac
            else:
                data['reportingfacility'] = reporting_facility

            print data['fTimeStamp'], data['latitude'], data['longitude'], data['course'], data['direction'], data['kts'], data['mph'], data['elevation'], data['ascrate'], data['reportingfacility']

            if len(data) == 10:
                retlist.append(data)

    return retlist
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