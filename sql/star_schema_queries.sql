
-- WeatherPulse: Star Schema Analytical Queries

-- Use the latest successful or partially successful ingestion run
-- so multiple forecast snapshots are not mixed together.

-- 1. City-wise Average Weather Summary
SELECT
    l.city_name,
    ROUND(AVG(f.temperature_2m), 2) AS avg_temperature,
    ROUND(AVG(f.relative_humidity_2m), 2) AS avg_humidity,
    ROUND(SUM(f.precipitation), 2) AS total_precipitation,
    MAX(f.wind_speed_10m) AS max_wind_speed
FROM fact_weather f
JOIN dim_location l
    ON f.location_key = l.location_key
WHERE f.source_run_id = (
    SELECT MAX(run_id)
    FROM ingestion_runs
    WHERE status IN ('SUCCESS', 'PARTIAL')
)
GROUP BY l.city_name
ORDER BY avg_temperature DESC;


-- 2. Date-wise Average Temperature
SELECT
    d.full_date,
    ROUND(AVG(f.temperature_2m), 2) AS avg_temperature
FROM fact_weather f
JOIN dim_date d
    ON f.date_key = d.date_key
WHERE f.source_run_id = (
    SELECT MAX(run_id)
    FROM ingestion_runs
    WHERE status IN ('SUCCESS', 'PARTIAL')
)
GROUP BY d.full_date
ORDER BY d.full_date;


-- 3. Hour-wise Average Temperature
SELECT
    t.hour,
    ROUND(AVG(f.temperature_2m), 2) AS avg_temperature
FROM fact_weather f
JOIN dim_time t
    ON f.time_key = t.time_key
WHERE f.source_run_id = (
    SELECT MAX(run_id)
    FROM ingestion_runs
    WHERE status IN ('SUCCESS', 'PARTIAL')
)
GROUP BY t.hour
ORDER BY t.hour;


-- 4. City-wise Total Precipitation
SELECT
    l.city_name,
    ROUND(SUM(f.precipitation), 2) AS total_precipitation_mm
FROM fact_weather f
JOIN dim_location l
    ON f.location_key = l.location_key
WHERE f.source_run_id = (
    SELECT MAX(run_id)
    FROM ingestion_runs
    WHERE status IN ('SUCCESS', 'PARTIAL')
)
GROUP BY l.city_name
ORDER BY total_precipitation_mm DESC;


-- 5. Top 5 Highest Wind Speed Records
SELECT
    l.city_name,
    d.full_date,
    t.hour,
    f.wind_speed_10m
FROM fact_weather f
JOIN dim_location l
    ON f.location_key = l.location_key
JOIN dim_date d
    ON f.date_key = d.date_key
JOIN dim_time t
    ON f.time_key = t.time_key
WHERE f.source_run_id = (
    SELECT MAX(run_id)
    FROM ingestion_runs
    WHERE status IN ('SUCCESS', 'PARTIAL')
)
ORDER BY f.wind_speed_10m DESC
LIMIT 5;


-- 6. City-wise Average Humidity
SELECT
    l.city_name,
    ROUND(AVG(f.relative_humidity_2m), 2) AS avg_humidity
FROM fact_weather f
JOIN dim_location l
    ON f.location_key = l.location_key
WHERE f.source_run_id = (
    SELECT MAX(run_id)
    FROM ingestion_runs
    WHERE status IN ('SUCCESS', 'PARTIAL')
)
GROUP BY l.city_name
ORDER BY avg_humidity DESC;
