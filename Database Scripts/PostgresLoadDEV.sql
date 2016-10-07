insert into dev.FlightLogs  (select * from public.Flightlogs);  
insert into dev.ScrapedFlights  (select * from public.ScrapedFlights);  
insert into dev.AllFlights  (select * from public.AllFlights);  
insert into dev.AllAirports  (select * from public.AllAirports);  
insert into dev.StatusType  (select * from public.StatusType);  