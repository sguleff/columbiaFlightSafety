--Create global list of all flights
DROP TABLE IF EXISTS FlightLogs;
DROP TABLE IF EXISTS public.ScrapedFlights;
DROP TABLE IF EXISTS public.AllFlights;
DROP TABLE IF EXISTS public.AllAirports;

CREATE TABLE public.AllAirports (
    id SERIAL primary key,
    AirportCode varchar(20) NOT NULL,
	AirportName varchar(100) NOT NULL,
	Status varchar(20) NOT NULL,
    date_added timestamp default NULL
);

ALTER TABLE public.AllAirports
  OWNER TO postgres;


CREATE TABLE public.AllFlights(
    id SERIAL primary key,
	AirportCode varchar(20) NOT NULL,
	ArrDepType varchar(10) NOT NULL,
    FlightNumber varchar(20) NOT NULL,
    date_added timestamp default NULL
);

ALTER TABLE public.AllFlights
  OWNER TO postgres;

--Create flights that need to be scraped
CREATE TABLE public.ScrapedFlights (
    id SERIAL primary key,
    AllFlightsId bigint references public.AllFlights(id), 
    FlightDate date default NULL,
    FlightNumber varchar(20) NOT NULL,
    AircraftType varchar(20) NOT NULL,
    Origin varchar(100) NOT NULL,
    Destination varchar(100) NOT NULL,
    Departure timestamp NOT NULL,
    Arrival timestamp NOT NULL,
    Duration varchar(20) NOT NULL,
    ZuluTime varchar(20) NOT NULL,
    DistancePlanned integer NOT NULL,
    DistanceFlown integer NOT NULL,
    DirectDistance integer NOT NULL,
    Route varchar(500) NOT NULL,
	Simulated boolean NOT NULL,
    Status varchar(20) NOT NULL,
    ScrapedBy varchar(20) NOT NULL,
    date_scraped date default NULL
);

ALTER TABLE public.ScrapedFlights
  OWNER TO postgres;


--Store Flight Log
CREATE TABLE FlightLogs (
    id SERIAL primary key,
    ScrapedFlights bigint references ScrapedFlights(id),
    UniversalTime timestamp NOT NULL,
	Latitude real NOT NULL,
	Longitude real NOT NULL,
	Course integer NOT NULL,
	Direction varchar(15) NOT NULL,
	KTS integer NOT NULL,
	MPH integer NOT NULL,
	Elevation integer NOT NULL,
	AscRate integer NULL,
	ReportingFacility varchar(100) NOT NULL,
	Simulated boolean NOT NULL,
    ScrapedBy timestamp default NULL,
    date_added timestamp default NULL
);

ALTER TABLE FlightLogs
  OWNER TO postgres;

--Test Code below
/*
insert into public.AllFlights (
    FlightNumber ,
    date_added) values ('UA88', '10/1/2016')
;

insert into public.ScrapedFlights (
    AllFlightsId , 
    FlightDate ,
    FlightNumber ,
    AircraftType ,
    Origin ,
    Destination ,
    Departure ,
    Arrival ,
    Duration ,
    ZuluTime ,
    Status ,
    ScrapedBy ,
    date_scraped 
) values (1 , 
    '9/30/2016' ,
    'UA88' ,
    '77734' ,
    'KDEN' ,
    'KLGA' ,
    '9/30/2016' ,
    '9/30/2016' ,
    'long flight' ,
    'Z1034' ,
    'SCRAPED' ,
    'SAM' ,
    '9/30/2016' );
*/
--insert into ScrapedFlights (Status,FlightNumber,FlightDate,date_scraped) values ('NOTSCRAPED','UA88','10/1/2016',NULL);