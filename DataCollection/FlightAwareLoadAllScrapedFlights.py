import FlightAwarePostgreCon as PGDBCon
import FlightAwareScrapeTest as PGScraper
   
###### THIS WILL REMOVE ALL EXISTING DATA
WIPE_EXISTING = False


def main():

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
            flight = PGDBCon.getNextFlight()

            if flight is None:
                break

            print "getting Flight:" +  flight

            #scrape all the arrivals into a list ['UAL88','UAL89']
            availableScrapes = PGScraper.getAvailableFlightHistory(flight.strip(" "))

            if len(availableScrapes) > 0:
                print "Loading Flight:" +  flight + " Total Lines: " + str(len(availableScrapes))
                PGDBCon.insertScrapableFlightList(availableScrapes)
                PGDBCon.setFlightScraped(flight)
            else:
                PGDBCon.setFlightScraped(flight,'ERROR')

        except:
            PGDBCon.setFlightScraped(flight,'ERROR')



if __name__ == "__main__":
    main()
