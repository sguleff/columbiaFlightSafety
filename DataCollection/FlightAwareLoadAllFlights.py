import FlightAwarePostgreCon as PGDBCon
import FlightAwareScrapeTest as PGScraper
   
###### THIS WILL REMOVE ALL EXISTING DATA
WIPE_EXISTING = False


#we should never run this module
def main():
    airportCode = ''

    try:
        if WIPE_EXISTING:
            PGDBCon.removeAllFlights()
            PGDBCon.setAllAirportsUnscraped()
    except:
        print "ERROR WIPING DATA"
    

    while True:
        try:
            #get the next available airport code
            airportCode = PGDBCon.getNextAirport()
            if airportCode == None:
                break

            #scrape all the arrivals into a list ['UAL88','UAL89']
            arrivals = PGScraper.getAllArrivingFlights(airportCode)
            if len(arrivals) > 0:
                PGDBCon.insertFlightList(airportCode, 'ARRIVALS', arrivals)
            else:
                PGDBCon.setAirportScraped(airportCode,'ERROR')
                continue

            #scrape all the arrivals into a list ['UAL88','UAL89']
            departures = PGScraper.getAllDepartingFlights(airportCode)
            if len(arrivals) > 0:
                PGDBCon.insertFlightList(airportCode, 'DEPARTURES', departures)
            else:
                PGDBCon.setAirportScraped(airportCode,'ERROR')


            PGDBCon.setAirportScraped(airportCode) 

        except:
            PGDBCon.setAirportScraped(airportCode,'ERROR')


if __name__ == "__main__":
    main()