-- Procedure to get next available airport and mark as Scraping
-- Returns Null when no airport is available
CREATE OR REPLACE FUNCTION fnGetNextAirport() 
RETURNS VARCHAR(20) as $airportCode$ 
declare
	code VARCHAR(20);
	thecount integer;
BEGIN
	SELECT count(*) into thecount FROM public.allairports WHERE Status = 'UNSCRAPED' limit 1;
	if (thecount > 0) Then
		SELECT airportCode into code FROM public.allairports WHERE Status = 'UNSCRAPED' limit 1;
		UPDATE public.allairports set Status = 'SCRAPING', date_added = NOW() where  AirportCode = code;
	end if;
	RETURN code;
END;
$airportCode$ LANGUAGE plpgsql;


-- Procedure to get next available airport and mark as Scraping
-- Returns Null when no airport is available
CREATE OR REPLACE FUNCTION fnGetNextFlight() 
RETURNS VARCHAR(20) as $FlightID$ 
declare
	code VARCHAR(20);
	thecount integer;
BEGIN
	SELECT count(*) into thecount FROM public.allflights WHERE Status = 'UNSCRAPED' limit 1;
	if (thecount > 0) Then
		SELECT flightnumber into code FROM public.allflights WHERE Status = 'UNSCRAPED' limit 1;
		UPDATE public.allflights set Status = 'SCRAPING', date_added = NOW() where flightnumber = code;
	end if;
	RETURN code;
END;
$FlightID$ LANGUAGE plpgsql;

-- Procedure to get next available Flight Log to scrape and mark as Scraping
-- Returns Null when no Flight Log is available
--SELECT id, allflightsid, flightdate, flightnumber, aircrafttype, origin, destination, departure, arrival, duration, zulutime, distanceplanned, distanceflown, directdistance, route, simulated, status, scrapedby, date_scraped
--	FROM public.scrapedflights;
CREATE OR REPLACE FUNCTION fnGetNextLog() 
RETURNS integer as $FlightID$ 
declare
	FlightId integer;
	thecount integer;
BEGIN
	SELECT count(*) into thecount FROM public.scrapedflights WHERE Status = 'UNSCRAPED' order by flightdate ASC limit 1;
	if (thecount > 0) Then
		SELECT flightnumber into FlightId FROM public.allflights WHERE Status = 'UNSCRAPED' order by flightdate ASC limit 1;
		UPDATE public.scrapedflights set Status = 'SCRAPING', date_added = NOW() where  id = FlightId;
	end if;
	RETURN FlightId;
END;
$FlightID$ LANGUAGE plpgsql;
