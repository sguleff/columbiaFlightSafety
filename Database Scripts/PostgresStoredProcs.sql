-- Procedure to insert a new city
CREATE OR REPLACE FUNCTION fnGetNextAirport() 
RETURNS VARCHAR(20) as $airportCode$ 
declare
	code VARCHAR(20);
	thecount integer;
BEGIN
	SELECT count(*) into thecount FROM public.allairports WHERE Status = 'UNSCRAPED' limit 1;
	if (thecount > 0) Then
		SELECT airportCode into code FROM public.allairports WHERE Status = 'UNSCRAPED' limit 1;
		UPDATE public.allairports set Status = 'SCRAPING' where  AirportCode = code;
	end if;
	RETURN code;

END;
$airportCode$ LANGUAGE plpgsql;
