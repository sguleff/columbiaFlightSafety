import psycopg2 as pg
import datetime

ConnectionString = "dbname='FlightAware' user='FlightAware_rw' host='104.45.131.212' password='*******'"




#UNSCRAPED/SCRAPED/SCRAPING/ERROR


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
        setAirportScraped(airportCode) 
        conn.commit()
    except:
        setAirportScraped(airportCode, 'ERROR') 
        conn.rollback()

    # Close communication with the database
    cur.close()
    conn.close()


#we should never run this module
def main():
    pass


if __name__ == "__main__":
    main()


