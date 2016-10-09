--Create global list of all flights
DROP TABLE IF EXISTS dev.FlightLogs;
DROP TABLE IF EXISTS dev.ScrapedFlights;
DROP TABLE IF EXISTS dev.AllFlights;
DROP TABLE IF EXISTS dev.AllAirports;
DROP TABLE IF EXISTS dev.StatusType;
DROP TABLE IF EXISTS dev.Runs;

CREATE TABLE dev.StatusType(
    id SERIAL primary key,
	SType varchar(10) unique NOT NULL

);

INSERT INTO dev.StatusType (SType) VALUES ('UNSCRAPED');
INSERT INTO dev.StatusType (SType) VALUES ('SCRAPED');
INSERT INTO dev.StatusType (SType) VALUES ('SCRAPING');
INSERT INTO dev.StatusType (SType) VALUES ('ERROR');

ALTER TABLE dev.StatusType
  OWNER TO postgres;



CREATE TABLE dev.Runs(
    id SERIAL primary key,
	RunType varchar(25),
    StartTime timestamp NOT NULL,
	EndTime timestamp NOT NULL,
	Status varchar(20) default 'UNSCRAPED' references dev.StatusType(SType)  NOT NULL,
    date_added timestamp default NOW()
);

ALTER TABLE dev.Runs
  OWNER TO postgres;



CREATE TABLE dev.AllAirports (
    id SERIAL primary key,
    AirportCode varchar(20) NOT NULL,
	AirportName varchar(100) NOT NULL,
	Status varchar(20) default 'UNSCRAPED' references dev.StatusType(SType)  NOT NULL,
	ScrapedBy varchar(20) default '' NOT NULL,
    date_added timestamp default NULL
);

ALTER TABLE dev.AllAirports
  OWNER TO postgres;


CREATE TABLE dev.AllFlights(
    id SERIAL primary key,
	AirportCode varchar(20) NOT NULL,
	ArrDepType varchar(10) NOT NULL,
    FlightNumber varchar(20)  NOT NULL,
	Status varchar(20) default 'UNSCRAPED'  references dev.StatusType(SType)  NOT NULL,
	ScrapedBy varchar(20) default '' NOT NULL,
    date_added timestamp default NULL
);

ALTER TABLE dev.AllFlights
  OWNER TO postgres;

--Create flights that need to be scraped
CREATE TABLE dev.ScrapedFlights (
    id SERIAL primary key,
    FlightDate date default NULL,
    FlightNumber varchar(20) NOT NULL,
    AircraftType varchar(20) NOT NULL,
    Origin varchar(10) NOT NULL,
    Destination varchar(10) NOT NULL,
    Departure timestamp NOT NULL,
    Arrival timestamp NOT NULL,
    DurationMin integer NOT NULL,
    ZuluTime varchar(20) NOT NULL,
    DistancePlanned integer NOT NULL,
    DistanceFlown integer NOT NULL,
    DirectDistance integer NOT NULL,
    Route varchar(500) NOT NULL,
	Simulated boolean default 'False' NOT NULL,
    Status varchar(20) default 'UNSCRAPED' references dev.StatusType(SType) NOT NULL,
    ScrapedBy varchar(20) default '' NOT NULL,
    date_scraped date default NULL
);

ALTER TABLE dev.ScrapedFlights
  OWNER TO postgres;


--Store Flight Log
CREATE TABLE dev.FlightLogs (
    id SERIAL primary key,
    ScrapedFlightsId bigint references ScrapedFlights(id),
    fTimeStamp timestamp NOT NULL,
	Latitude real NOT NULL,
	Longitude real NOT NULL,
	Course integer NOT NULL,
	Direction varchar(15) NOT NULL,
	KTS integer,
	MPH integer,
	Elevation integer,
	AscRate integer,
	ReportingFacility varchar(100) NOT NULL,
	Simulated boolean default 'False' NOT NULL,
    ScrapedBy varchar(20) default NULL,
    date_updated timestamp default NULL
);

ALTER TABLE dev.FlightLogs
  OWNER TO postgres;

--Test Code below
/*
insert into dev.AllFlights (
    FlightNumber ,
    date_updated) values ('UA88', '10/1/2016')
;

insert into dev.ScrapedFlights (
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
