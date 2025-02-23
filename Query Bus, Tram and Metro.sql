-- Tram
select DISTINCT gt.trip_id, gt.stop_id, st.stop_headsign, gt.stop_sequence, s.stop_name, gt.arrival_time, gt.arrival_delay,
	gt.departure_delay, gt.departure_time, gt.route_id
from gtfs_15_2024_15 AS gt
JOIN stops AS s USING (stop_id)
JOIN stop_times AS st USING (trip_id)
WHERE s.stop_name IN ('Liljeholmen', 'Årstadal', 'Årstaberg', 'Årstafältet', 'Valla torg', 'Linde', 'Globen', 'Gullmarsplan')
	 AND stop_headsign = 'Sickla'
ORDER BY trip_id, stop_sequence, arrival_time;


-- Metro

SELECT DISTINCT gt.trip_id, gt.stop_id, st.stop_headsign, gt.stop_sequence, s.stop_name, gt.arrival_time, gt.arrival_delay,
	gt.departure_delay, gt.departure_time 
from gtfs_15_2024_15 AS gt
JOIN stops AS s USING (stop_id)
JOIN stop_times AS st USING (trip_id)
WHERE stop_name IN ('Liljeholmen', 'Hornstull', 'Zinkensdamm', 'Mariatorget', 'Slussen') 
      AND stop_headsign IN ('Ropsten', 'Mörby centrum')
ORDER BY trip_id, stop_sequence;


SELECT DISTINCT gt.trip_id, gt.stop_id, st.stop_headsign, gt.stop_sequence, s.stop_name, gt.arrival_time, gt.arrival_delay,
	gt.departure_delay, gt.departure_time 
from gtfs_15_2024_15 AS gt
JOIN stops AS s USING (stop_id)
JOIN stop_times AS st USING (trip_id)
WHERE stop_name IN ('Slussen', 'Medborgarplatsen', 'Skanstull', 'Gullmarsplan') 
      AND stop_headsign IN ('Hagsätra', 'Farsta strand', 'Skarpnäck') 
ORDER BY trip_id, stop_sequence;


-- bus
SELECT DISTINCT gt.trip_id, gt.stop_id, st.stop_headsign, gt.stop_sequence, s.stop_name, gt.arrival_time, gt.arrival_delay, s.platform_code,
	gt.departure_delay, gt.departure_time 
from gtfs_15_2024_15 AS gt
JOIN stops AS s USING (stop_id)
JOIN stop_times AS st USING (trip_id)
WHERE stop_name IN ('Liljeholmen', 'Sjövikstorget', 'Sjöviksvägen', 'Hildebergsvägen', 'Årstaberg') 
      AND stop_headsign IN ('Östbergahöjden') 
ORDER BY trip_id, stop_sequence;


SELECT DISTINCT gt.trip_id, gt.stop_id, st.stop_headsign, gt.stop_sequence, s.stop_name, gt.arrival_time, gt.arrival_delay, s.platform_code,
	gt.departure_delay, gt.departure_time 
from gtfs_15_2024_15 AS gt
JOIN stops AS s USING (stop_id)
JOIN stop_times AS st USING (trip_id)
WHERE stop_name IN ('Årstaberg', 'Årsta gård', 'Ottsjövägen', 'Åmänningevägen', 'Årsta torg'
	'Årstaskolan', 'Vättersvägen', 'Skagersvägen', 'Sköntorpsplan', 'Gullmarsplan'  ) 
      AND stop_headsign IN ('Gullmarsplan') AND gt.stop_id IN ('9022001013235001','9022001013124001', '9022001013126002', '9022001013213001',
	'9022001013215000', '9021001013117000','9022001013111002','9022001013109002','9022001013105002', '9022001011725024')
ORDER BY trip_id, stop_sequence;