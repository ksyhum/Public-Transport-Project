copy gtfs_rt(trip_id,ROUTE_ID, stop_sequence, stop_id, arrival_delay, arrival_time, departure_delay, departure_time) 
	FROM 'E:\belajar GTFS RT\Belajar GTFS RT\data_with_tripandroute.csv' DELIMITER ',' CSV HEADER;

COPY GTFS_15_2024_15 FROM 'D:\Humam\KTH\Public Transport\Liljelhomen - Gummarsplan Project\Koda Real Time\Jan 2024\From Web\Result\15-01-2024\final_data_processed.csv' DELIMITER ',' CSV HEADER;



CREATE TABLE IF NOT EXISTS GTFS_15_2024_15 (
	trip_id TEXT,
	route_id TEXT,
	stop_sequence INT,
    stop_id TEXT,
    arrival_delay NUMERIC,
    arrival_time timestamptz,
    departure_delay NUMERIC,
    departure_time timestamptz,
    FOREIGN KEY (stop_id) REFERENCES stops(stop_id)
);



