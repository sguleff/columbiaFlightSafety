import FlightAwarePostgreCon as PGDBCon
import FlightAwareScrapeTest as PGScraper

###### THIS WILL REMOVE ALL EXISTING DATA
WIPE_EXISTING = False
SIMULATE = False

def main():

    if SIMULATE:
        #data = PGScraper.simulateGetAvailableFlightHistory()
        #PGDBCon.insertScrapableFlightList(data)
        id = PGDBCon.getNextScrapableFlight()
        flightDetails = PGDBCon.getNextScrapableFlightDetails(id)
        availableScrapes = PGScraper.getFlightTrackLog(*flightDetails)
        PGDBCon.insertFlightLogs(id, availableScrapes)
        return


    try:
        if WIPE_EXISTING:
            PGDBCon.removeAllLogs()
            PGDBCon.setAllScrapableFlightsUnscraped()
            return
    except:
        print "ERROR WIPING DATA"


    while True:
        try:
            #get the next available airport code
            id = PGDBCon.getNextScrapableFlight()
            if id is None:
                break

            flightDetails = PGDBCon.getNextScrapableFlightDetails(id)

            #scrape all available information about flight with ScrapedFlights.id == id
            availableScrapes = PGScraper.getFlightTrackLog(*flightDetails)

            if availableScrapes:
                PGDBCon.insertFlightLogs(id, availableScrapes)
                PGDBCon.setScrapableFlightScraped(id)
            else:
                PGDBCon.setScrapableFlightScraped(id, 'ERROR')

        except:
            PGDBCon.setScrapableFlightScraped(id, 'ERROR')


if __name__ == "__main__":
    main()
