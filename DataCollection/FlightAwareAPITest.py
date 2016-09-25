#Sample FlightAware code created by Sam Guleff


import sys
from suds import null, WebFault
from suds.client import Client
import logging

username = 'user'
apiKey = '*******************************'
url = 'http://flightxml.flightaware.com/soap/FlightXML2/wsdl'

logging.basicConfig(level=logging.INFO)
api = Client(url, username=username, password=apiKey)
#print api


# Get the flights enroute
enroute = api.service.Enroute('KDEN',10,'',0)

flights = enroute['enroute']

print "Aircraft en route to KDEN:"
for flight in flights:
    print str(flight['actualdeparturetime'])+ '\t' + \
	str(flight['aircrafttype'])+ '\t' + \
	str(flight['destination'])+ '\t' + \
	str(flight['destinationCity'])+ '\t' +\
	str(flight['destinationName'])+ '\t' + \
	str(flight['estimatedarrivaltime'])+ '\t' + \
	str(flight['filed_departuretime'])+ '\t' + \
	str(flight['ident'])+ '\t' + \
	str(flight['origin'])+ '\t' + \
	str(flight['originCity'])+ '\t' + \
	str(flight['originName'])+ '\t' 


    #z = api.service.SearchBirdseyePositions(howMany=10, query='= dest KLAX')
