import psycopg2 as pg
import datetime
import GlobalSettings

ConnectionString = GlobalSettings.ConnectionString
#environment = GlobalSettings.ENVIRONMENT

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
        if i is None:
            retString += 'NULL, '
        else:
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
    '''Locks an airport code to Scraping and returns airport code'''
    try:
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
        cur.execute("""Update public.allairports set Status = %s, date_added = NOW() where AirportCode = %s  """, (status,airportCode) )
        if status == 'ERROR':
            cur.execute("""Delete from public.AllFlights where AirportCode = %s  """, (airportCode,) )
        conn.commit()
    except:
        conn.rollback()

    # Close communication with the database
    cur.close()
    conn.close()

def setAllAirportsUnscraped():
    '''updates public.allairports table and sets them to UNSCRAPED'''
    try:
        conn = pg.connect(ConnectionString)
        cur = conn.cursor()
        cur.execute(""" Update public.allairports set status = 'UNSCRAPED' """)
        conn.commit()
    except:
        conn.rollback()

    # Close communication with the database
    cur.close()
    conn.close()

#Flight Related Methods
def removeAllFlights():
    ''' delete from  AllFlights table all records will be removed'''
    try:
        conn = pg.connect(ConnectionString)
        cur = conn.cursor()
        cur.execute("""  delete from  public.allflights;""")
        conn.commit()
    except:
        conn.rollback()

    # Close communication with the database
    cur.close()
    conn.close()

def setAllFlightsUnscraped():
    '''updates public.allflights table and sets them to UNSCRAPED'''
    try:
        conn = pg.connect(ConnectionString)
        cur = conn.cursor()
        cur.execute(""" Update public.allflights set status = 'UNSCRAPED' """)
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
            data.append((airportCode, ArrDepType, flight))
        conn = pg.connect(ConnectionString)
        cur = conn.cursor()
        for row in data:
            cur.execute("""INSERT INTO public.AllFlights (AirportCode, ArrDepType, FlightNumber) VALUES (%s,%s,%s)""" , row)
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
            #cur.execute("""Delete from {0}.ScrapedFlights where FlightNumber = %s """.format(environment), (FlightNumber,) )
            cur.execute("""Delete from public.ScrapedFlights where FlightNumber = %s """, (FlightNumber,) )
        conn.commit()
    except Exception:
        conn.rollback()

    # Close communication with the database
    cur.close()
    conn.close()

#Scrapable Flights related
def removeAllscrapable():
    ''' delete from  AllFlights table all records will be removed'''
    try:
        conn = pg.connect(ConnectionString)
        cur = conn.cursor()
        cur.execute("""  delete from  public.scrapedflights;""")
        conn.commit()
    except:
        conn.rollback()

    # Close communication with the database
    cur.close()
    conn.close()

def setAllScrapableFlightsUnscraped():
    '''updates public.allflights table and sets them to UNSCRAPED'''
    try:
        conn = pg.connect(ConnectionString)
        cur = conn.cursor()
        cur.execute(""" Update public.scrapedflights set status = 'UNSCRAPED' """)
        conn.commit()
    except:
        conn.rollback()

    # Close communication with the database
    cur.close()
    conn.close()

def getNextFlight():
    '''gets the flight number of the next flight and sets status to scraping'''
    try:
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
            row['ScrapedBy'] = GlobalSettings.SCRAPER_ID
            cur.execute("""INSERT INTO public.ScrapedFlights """ + dicttoInsert(row))
        conn.commit()
    except:
        setFlightScraped(airportCode, 'ERROR')
        conn.rollback()

    # Close communication with the database
    cur.close()
    conn.close()

def setScrapableFlightScraped(id = -1, status = 'SCRAPED'):
    '''set ScrapedFlights as UNSCRAPED/SCRAPED/SCRAPING/ERROR'''
    try:
        conn = pg.connect(ConnectionString)
        cur = conn.cursor()
        cur.execute("""Update public.scrapedFlights set Status = %s, date_scraped = NOW() where id = %s  """, (status, id) )
        if status == 'ERROR':
            cur.execute("""Delete from public.flightLogs where ScrapedFlightsId = %s  """, (id,) )
        conn.commit()
    except:
        conn.rollback()

    # Close communication with the database
    cur.close()
    conn.close()

#Log related

def getNextScrapableFlight():
    try:
        '''Locks a flight number to Scraping and returns airport code'''
        conn = pg.connect(ConnectionString)
        cur = conn.cursor()
        cur.execute("select * from public.fnGetNextLog();")
        rows = cur.fetchall()
        cur.close()
        conn.commit()
        conn.close()
        if len(rows) > 0:
            return rows[0][0]
        else:
            return None
    except Exception:
        conn.rollback()

    # Close communication with the database
    cur.close()
    conn.close()

 #(date = '', FlightNumber = '', ZuluTime = '', DepartureAirportCode = '', ArrivalAirportCode = '') RPAD(numcol::text, 3, '0')

def getNextScrapableFlightDetails(id = -1):
    '''Returns tuple of data needed to scrape a flight based on the id field of the flight'''
    try:
        '''Locks a flight number to Scraping and returns airport code'''
        conn = pg.connect(ConnectionString)
        cur = conn.cursor()
        cur.execute("select cast(date_part('year',FlightDate) as text) || LPAD(cast(date_part('month',FlightDate) as text),2,'0') || LPAD(cast (date_part('day',FlightDate) as text),2,'0') as formatedFlightDate, FlightNumber, ZuluTime, Origin as DepartureAirportCode,  Destination as ArrivalAirportCode from public.scrapedFlights where id = " + str(id))
        rows = cur.fetchall()
        cur.close()
        conn.close()
        if len(rows) > 0:
            return (rows[0][0], rows[0][1], rows[0][2], rows[0][3], rows[0][4])
        else:
            return None
    except:
        conn.rollback()

    # Close communication with the database
    cur.close()
    conn.close()

def removeAllLogs():
    ''' delete from All flightLogs table all records will be removed'''
    try:
        conn = pg.connect(ConnectionString)
        cur = conn.cursor()
        cur.execute(""" delete from public.flightLogs;""")
        conn.commit()
    except:
        conn.rollback()

    # Close communication with the database
    cur.close()
    conn.close()

def insertFlightLogs(id = -1, data = []):
    '''Inserts flight Logs into public.FlightLogs data
    should be a list of dict of all required fields and values'''
    try:
        conn = pg.connect(ConnectionString)
        cur = conn.cursor()
        for row in data:
            row['date_updated'] = str(datetime.datetime.now() + datetime.timedelta(hours=4))
            row['ScrapedFlightsId'] = id
            row['ScrapedBy'] = GlobalSettings.SCRAPER_ID
            cur.execute("""INSERT INTO public.FlightLogs """ + dicttoInsert(row))

        conn.commit()
    except Exception:
        setScrapableFlightScraped(id, 'ERROR')
        conn.rollback()

    # Close communication with the database
    cur.close()
    conn.close()


#we should never run this module
def main():
    pass

if __name__ == "__main__":
    main()
