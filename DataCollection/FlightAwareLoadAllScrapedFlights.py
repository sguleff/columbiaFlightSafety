import FlightAwarePostgreCon as PGDBCon
import FlightAwareScrapeTest as PGScraper
   
###### THIS WILL REMOVE ALL EXISTING DATA
WIPE_EXISTING = False


def main():
    airportCode = ''

    try:
        if WIPE_EXISTING:
            PGDBCon.removeAllscrapable()
            PGDBCon.setAllFlightsUnscraped()
            return
    except:
        print "ERROR WIPING DATA"
    

    while True:
        try:
            #get the next available airport code
            flight = PGDBCon.getNextFlight().strip(" ")
            if flight == None:
                break

            #scrape all the arrivals into a list ['UAL88','UAL89']
            availableScrapes = PGScraper.getAvailableFlightHistory(flight)

            #availableScrapes = PGScraper.simulateGetAvailableFlightHistory()
            #PGDBCon.insertScrapableFlightList(availableScrapes)

            if len(availableScrapes) > 0:
                PGDBCon.insertScrapableFlightList(availableScrapes)
            else:
                PGDBCon.setFlightScraped(flight,'ERROR')
                continue

            PGDBCon.setFlightScraped(flight)

        except:
            PGDBCon.setFlightScraped(flight,'ERROR')


if __name__ == "__main__":
    main()



