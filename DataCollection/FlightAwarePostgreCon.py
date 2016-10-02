import psycopg2 as pg
import datetime

ConnectionString = "dbname='FlightAware' user='FlightAware_rw' host='104.45.131.212' password='******'"



#UNSCRAPED/SCRAPED/SCRAPING/ERROR
def insertAirports(Airports = []):
    '''Truncates then imports into airports table all records'''
    try:
        conn = pg.connect(ConnectionString)
    except:
        return

    cur = conn.cursor()

    cur.execute(""" truncate public.allairports;""")
    cur.executemany("""INSERT INTO public.allairports (AirportCode, AirportName, Status, date_added) VALUES (%s,%s,%s,%s)""" ,Airports)
    conn.commit()


def getNextAirport():
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



def setAirportScraped(airportCode = '', status = 'SCRAPED'):
    '''set airport as UNSCRAPED/SCRAPED/SCRAPING/ERROR'''
    try:
        conn = pg.connect(ConnectionString)
    except:
        return

    cur = conn.cursor()

    cur.executemany("""Update public.allairports set Status = %s where  AirportCode = %s  """, (status,airportCode) )
    conn.commit()




def insertFlights(Flights = []):
    try:
        conn = pg.connect(ConnectionString)
    except:
        return

    cur = conn.cursor()


    cur.executemany("""INSERT INTO public.AllFlights (flightnumber, date_added) VALUES (%s,%s)""" ,Flights)
    conn.commit()

#we should never run this module
def main():

    insertFlights([('UA88','1/1/1901'),('UA89','1/1/1901')])



    return




    try:
        conn = pg.connect(ConnectionString)
    except:
        return

    cur = conn.cursor()

    cur.execute("""SELECT * from public.AllFlights""")
    rows = cur.fetchall()
    for row in rows:
        print "   ", row


    flightNumber = 'UA888'
    datestr = '10/1/2016'
    cur.execute('INSERT INTO public.AllFlights (FlightNumber, date_added) VALUES (%s, %s)', (flightNumber, datestr))
    conn.commit()

if __name__ == "__main__":
    main()


