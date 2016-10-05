import FlightAwarePostgreCon as PGDBCon
import FlightAwareScrapeTest as PGScraper
   
###### THIS WILL REMOVE ALL EXISTING DATA
WIPE_EXISTING = False
SIMULATE = False

def main():

    if SIMULATE:
        data = PGScraper.simulateGetAvailableFlightHistory()
        PGDBCon.insertScrapableFlightList(data)
        id = PGDBCon.getNextScrapableFlight()
        flightDetails = PGDBCon.getNextScrapableFlightDetails(id)
        availableScrapes = PGScraper.getFlightTrackLog(flightDetails[0],flightDetails[1],flightDetails[2],flightDetails[3],flightDetails[4] )
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
            if id == None:
                break

            flightDetails = PGDBCon.getNextScrapableFlightDetails(id)

            #scrape all the arrivals into a list ['UAL88','UAL89']
            availableScrapes = PGScraper.getFlightTrackLog(flightDetails[0],flightDetails[1],flightDetails[2],flightDetails[3],flightDetails[4] )

         
            if len(availableScrapes) > 0:
                PGDBCon.insertFlightLogs(availableScrapes)
            else:
                PGDBCon.setScrapableFlightScraped(id,'ERROR')
                continue

            PGDBCon.setScrapableFlightScraped(id)

        except:
            PGDBCon.setScrapableFlightScraped(id,'ERROR')


if __name__ == "__main__":
    main()



