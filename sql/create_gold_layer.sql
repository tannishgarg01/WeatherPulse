
-- WeatherPulse: Gold Layer
-- Dashboard-ready analytical views

-- 1. City-wise Weather Summary
CREATE VIEW IF NOT EXISTS gold_city_weather_summary AS
SELECT
    l.city_name,
    ROUND(AVG(f.temperature_2m), 2) AS avg_temperature,
    ROUND(MIN(f.temperature_2m), 2) AS min_temperature,
    ROUND(MAX(f.temperature_2m), 2) AS max_temperature,
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
GROUP BY l.city_name;


-- 2. Daily Weather Trend
CREATE VIEW IF NOT EXISTS gold_daily_weather_trend AS
SELECT
    d.full_date,
    ROUND(AVG(f.temperature_2m), 2) AS avg_temperature,
    ROUND(AVG(f.relative_humidity_2m), 2) AS avg_humidity,
    ROUND(SUM(f.precipitation), 2) AS total_precipitation,
    MAX(f.wind_speed_10m) AS max_wind_speed
FROM fact_weather f
JOIN dim_date d
    ON f.date_key = d.date_key
WHERE f.source_run_id = (
    SELECT MAX(run_id)
    FROM ingestion_runs
    WHERE status IN ('SUCCESS', 'PARTIAL')
)
GROUP BY d.full_date;


-- 3. Hourly Weather Trend
CREATE VIEW IF NOT EXISTS gold_hourly_weather_trend AS
SELECT
    t.hour,
    ROUND(AVG(f.temperature_2m), 2) AS avg_temperature,
    ROUND(AVG(f.relative_humidity_2m), 2) AS avg_humidity,
    ROUND(AVG(f.wind_speed_10m), 2) AS avg_wind_speed
FROM fact_weather f
JOIN dim_time t
    ON f.time_key = t.time_key
WHERE f.source_run_id = (
    SELECT MAX(run_id)
    FROM ingestion_runs
    WHERE status IN ('SUCCESS', 'PARTIAL')
)
GROUP BY t.hour;
