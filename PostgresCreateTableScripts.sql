--Create global list of all flights
DROP TABLE IF EXISTS public.AllFlights;
CREATE TABLE public.AllFlights (
    id SERIAL primary key,
    FlightNumber varchar(20) NOT NULL,
    date_added timestamp default NULL
);

ALTER TABLE public.AllFlights
  OWNER TO postgres;

--Create flights that need to be scraped
DROP TABLE IF EXISTS public.ScrapedFlights;
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
    Route varchar(500) NULL,
    Status varchar(20) NOT NULL,
    ScrapedBy varchar(20) NOT NULL,
    date_scraped date default NULL
);

ALTER TABLE public.ScrapedFlights
  OWNER TO postgres;


--Store Flight Log
DROP TABLE IF EXISTS FlightLogs;
CREATE TABLE FlightLogs (
    id SERIAL primary key,
    ScrapedFlights bigint references ScrapedFlights(id),
    FlightNumber varchar(20) NOT NULL,
    AircraftType varchar(20) NOT NULL,
    Origin varchar(100) NOT NULL,
    Destination varchar(100) NOT NULL,
    Departure timestamp NOT NULL,
    Arrival timestamp NOT NULL,
    Duration varchar(20) NOT NULL,
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