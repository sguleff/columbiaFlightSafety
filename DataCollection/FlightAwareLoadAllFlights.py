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
            if airportCode is None:
                break

            #scrape all the arrivals into a set {'UAL88','UAL89'}
            arrivals = PGScraper.getAllArrivingFlights(airportCode)

            #scrape all the departures into a set {'UAL88','UAL89'}
            departures = PGScraper.getAllDepartingFlights(airportCode)

            # if there's more than 0 arrivals and more than 0 departures, populate table allflights with those and set airport status to 'SCRAPED'
            if arrivals and departures:
                PGDBCon.insertFlightList(airportCode, 'ARRIVALS', arrivals)
                PGDBCon.insertFlightList(airportCode, 'DEPARTURES', departures)
                PGDBCon.setAirportScraped(airportCode)
            else:
                PGDBCon.setAirportScraped(airportCode,'ERROR')

        except:
            PGDBCon.setAirportScraped(airportCode,'ERROR')


if __name__ == "__main__":
    main()
