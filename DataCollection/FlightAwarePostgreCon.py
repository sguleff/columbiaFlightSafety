import psycopg2 as pg
import datetime

ConnectionString = "dbname='FlightAware' user='FlightAware_rw' host='104.45.131.212' password='Asdewq123$'"



#UNSCRAPED/SCRAPED/SCRAPING/ERROR

def insertAirports(Airports = []):
    '''imports into airports table many records'''
    try:
        conn = pg.connect(ConnectionString)
    except:
        return

    cur = conn.cursor()

    cur.executemany("""INSERT INTO public.allairports (AirportCode, AirportName, Status, date_added) VALUES (%s,%s,%s,%s)""" ,Airports)
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


