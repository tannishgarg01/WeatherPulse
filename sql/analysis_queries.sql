
-- WeatherPulse: SQL Analysis Queries

-- 1. City-wise Average Temperature
SELECT
    l.city_name,
    ROUND(AVG(w.temperature_2m), 2) AS avg_temperature
FROM weather_forecasts w
JOIN locations l
    ON w.location_id = l.location_id
GROUP BY l.city_name
ORDER BY avg_temperature DESC;


-- 2. Maximum Temperature Recorded in Each City
SELECT
    l.city_name,
    MAX(w.temperature_2m) AS max_temperature
FROM weather_forecasts w
JOIN locations l
    ON w.location_id = l.location_id
GROUP BY l.city_name
ORDER BY max_temperature DESC;


-- 3. Minimum Temperature Recorded in Each City
SELECT
    l.city_name,
    MIN(w.temperature_2m) AS min_temperature
FROM weather_forecasts w
JOIN locations l
    ON w.location_id = l.location_id
GROUP BY l.city_name
ORDER BY min_temperature ASC;


-- 4. Total Forecast Precipitation by City
SELECT
    l.city_name,
    ROUND(SUM(w.precipitation), 2) AS total_precipitation_mm
FROM weather_forecasts w
JOIN locations l
    ON w.location_id = l.location_id
GROUP BY l.city_name
ORDER BY total_precipitation_mm DESC;


-- 5. Maximum Wind Speed by City
SELECT
    l.city_name,
    MAX(w.wind_speed_10m) AS max_wind_speed_kmh
FROM weather_forecasts w
JOIN locations l
    ON w.location_id = l.location_id
GROUP BY l.city_name
ORDER BY max_wind_speed_kmh DESC;


-- 6. Average Humidity by City
SELECT
    l.city_name,
    ROUND(AVG(w.relative_humidity_2m), 2) AS avg_humidity
FROM weather_forecasts w
JOIN locations l
    ON w.location_id = l.location_id
GROUP BY l.city_name
ORDER BY avg_humidity DESC;
