import psycopg2 as pg
import datetime

ConnectionString = "dbname='FlightAware' user='FlightAware_rw' host='104.45.131.212' password='********'"

#UNSCRAPED/SCRAPED/SCRAPING/ERROR

#supporting methods

def dicttoInsert(data = {}):
    retString = '('
    listvalues = []
    listkeys = []
    for k, v in data.iteritems():
        listvalues.append(v)
        listkeys.append(k)

    for i in listkeys:
        retString += str(i) + ', '

    retString = retString[:-2] + ') VALUES ('

    for i in listvalues:
        if type(i) is int or type(i) is float or type(i) is long or type(i) is complex :
            retString += ' ' + str(i) + ', '
        else:
            retString += '\'' + str(i) + '\', '
    retString = retString[:-2] + ')'
    return retString

#Airport Related Methods
def insertAirports(Airports = []):
    '''Truncates then imports into airports table all records'''
    try:
        conn = pg.connect(ConnectionString)
        cur = conn.cursor()
        cur.execute(""" truncate public.allairports;""")
        cur.executemany("""INSERT INTO public.allairports (AirportCode, AirportName, Status, date_added) VALUES (%s,%s,%s,%s)""" ,Airports)
        conn.commit()
    except:
        conn.rollback()

    # Close communication with the database
    cur.close()
    conn.close()

def getNextAirport():
    try:
        '''Locks an airport code to Scraping and returns airport code'''
        conn = pg.connect(ConnectionString)
        cur = conn.cursor()
        cur.callproc("public.fngetnextairport")
        rows = cur.fetchall()
        cur.close()
        conn.commit()
        conn.close()
        if len(rows) > 0:
            airportCode = rows[0][0]
            return airportCode
        else:
            return None
    except:
        conn.rollback()

    # Close communication with the database
    cur.close()
    conn.close()

def setAirportScraped(airportCode = '', status = 'SCRAPED'):
    '''set airport as UNSCRAPED/SCRAPED/SCRAPING/ERROR'''
    try:
        conn = pg.connect(ConnectionString)
        cur = conn.cursor()
        cur.execute("""Update public.allairports set Status = %s where  AirportCode = %s  """, (status,airportCode) )
        if status == 'ERROR':
            cur.execute("""Delete from public.AllFlights where AirportCode = %s  """, (airportCode) )
        conn.commit()
    except:
        conn.rollback()

    # Close communication with the database
    cur.close()
    conn.close()

#Flight Related Methods
def removeAllFlights():
    '''Truncates AllFlights table all records will be removed'''
    try:
        conn = pg.connect(ConnectionString)
        cur = conn.cursor()
        cur.execute(""" truncate public.allflights;""")
        conn.commit()
    except:
        conn.rollback()

    # Close communication with the database
    cur.close()
    conn.close()

def insertFlightList(airportCode = '', ArrDepType = '', flightsfound = []):
    try:
        data = []
        for flight in flightsfound:
            data.append((airportCode, ArrDepType, flight, str(datetime.datetime.now())))
        conn = pg.connect(ConnectionString)
        cur = conn.cursor()
        for row in data:
            cur.execute("""INSERT INTO public.AllFlights (AirportCode, ArrDepType, FlightNumber, date_added) VALUES (%s,%s,%s,%s)""" , row)
        conn.commit()
    except:
        setAirportScraped(airportCode, 'ERROR') 
        conn.rollback()

    # Close communication with the database
    cur.close()
    conn.close()

def setFlightScraped(FlightNumber = '', status = 'SCRAPED'):
    '''set airport as UNSCRAPED/SCRAPED/SCRAPING/ERROR'''
    try:
        conn = pg.connect(ConnectionString)
        cur = conn.cursor()
        cur.execute("""Update public.AllFlights set Status = %s where  FlightNumber = %s  """, (status,FlightNumber) )
        if status == 'ERROR':
            cur.execute("""Delete from public.ScrapedFlights where FlightNumber = %s  """, (FlightNumber) )
        conn.commit()
    except:
        conn.rollback()

    # Close communication with the database
    cur.close()
    conn.close()


#Scrapable Flights related
def removeAllscrapable():
    '''Truncates AllFlights table all records will be removed'''
    try:
        conn = pg.connect(ConnectionString)
        cur = conn.cursor()
        cur.execute(""" truncate public.scrapedflights;""")
        conn.commit()
    except:
        conn.rollback()

    # Close communication with the database
    cur.close()
    conn.close()

def getNextFlight():
    try:
        '''Locks a flight number to Scraping and returns airport code'''
        conn = pg.connect(ConnectionString)
        cur = conn.cursor()
        cur.callproc("public.fnGetNextFlight")
        rows = cur.fetchall()
        cur.close()
        conn.commit()
        conn.close()
        if len(rows) > 0:
            return rows[0][0]
        else:
            return None
    except:
        conn.rollback()

    # Close communication with the database
    cur.close()
    conn.close()

def insertScrapableFlightList(data = []):
    '''Inserts scrapable flights into public.ScrapedFlights data 
    should be a list of dict of all required fields and values'''
    try:
        conn = pg.connect(ConnectionString)
        cur = conn.cursor()
        for row in data:
            row['date_scraped'] = str(datetime.datetime.now())
            cur.execute("""INSERT INTO public.ScrapedFlights """ + dicttoInsert(row))
        conn.commit()
    except:
        setFlightScraped(airportCode, 'ERROR') 
        conn.rollback()

    # Close communication with the database
    cur.close()
    conn.close()

#we should never run this module
def main():
    pass


if __name__ == "__main__":
    main()
