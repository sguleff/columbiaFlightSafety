import FlightAwareScrapeTest as FAScraper

flightData = []
ArrivingFlights = {}
ScrapableFlights = []


def main():
    '''moreFlights = FAScraper.getAvailableFlightHistory('UAL88') #
    for availableFlight in moreFlights:
        flightLog = FAScraper.getFlightTrackLog2(availableFlight)
        print 'did it'
    return '''


    #get all arriving flights to airport
    arrivingFlights = FAScraper.getAllArrivingFlights('KEWR', 40)
    departingFlights = FAScraper.getAllDepartingFlights('KEWR', 40)


    #find all scrapable flights
    for flightNumber, scraped in arrivingFlights.iteritems():
        if not scraped:
            moreFlights = FAScraper.getAvailableFlightHistory(flightNumber) #'UAL88'
            for appendFlights in moreFlights:
                ScrapableFlights.append(appendFlights)

    #get all flight logs
    for availableFlight in ScrapableFlights:
        flightLog = FAScraper.getFlightTrackLog2(availableFlight)
        if flightLog is not None:
            flightData.append(flightLog) #load to database and flag as scraped

if __name__ == "__main__":
    main()