import psycopg2 as pg


#we should never run this module
def main():
    try:
        conn = pg.connect("dbname='FlightAware' user='FlightAware_rw' host='104.45.131.212' password='*******'")
    except:
        print "I am unable to connect to the database"

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
