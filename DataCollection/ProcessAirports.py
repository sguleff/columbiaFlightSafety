#this is to load all airports into the database
import FlightAwarePostgreCon as FADBCon
import os 
import datetime

#we should never run this module
def main():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file = open('rawAirports.txt', 'r')

    lines = file.readlines()
    airportLoad = []
    for line in lines:
        split = str.split(line,'(')
        if len(split) > 1:
            code = str.replace(split[1],')',' ').strip()
            airportName  = str.replace(split[0],')',' ').strip()
            print 'K' + code
            airportLoad.append(('K' + code, airportName, 'UNSCRAPED', datetime.datetime.now()))
            

    FADBCon.insertAirports(airportLoad)

if __name__ == "__main__":
    main()