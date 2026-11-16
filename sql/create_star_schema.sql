
-- WeatherPulse: Star Schema Tables

PRAGMA foreign_keys = ON;

-- 1. Location Dimension
CREATE TABLE IF NOT EXISTS dim_location (
    location_key INTEGER PRIMARY KEY AUTOINCREMENT,
    city_name TEXT NOT NULL UNIQUE,
    latitude REAL,
    longitude REAL,
    timezone TEXT,
    country TEXT
);

-- 2. Date Dimension
CREATE TABLE IF NOT EXISTS dim_date (
    date_key INTEGER PRIMARY KEY,
    full_date TEXT NOT NULL UNIQUE,
    day INTEGER NOT NULL,
    month INTEGER NOT NULL,
    month_name TEXT NOT NULL,
    year INTEGER NOT NULL,
    day_of_week TEXT NOT NULL
);

-- 3. Time Dimension
CREATE TABLE IF NOT EXISTS dim_time (
    time_key INTEGER PRIMARY KEY,
    hour INTEGER NOT NULL,
    minute INTEGER NOT NULL,
    time_period TEXT NOT NULL,
    UNIQUE(hour, minute)
);

-- 4. Weather Fact Table
CREATE TABLE IF NOT EXISTS fact_weather (
    weather_key INTEGER PRIMARY KEY AUTOINCREMENT,

    location_key INTEGER NOT NULL,
    date_key INTEGER NOT NULL,
    time_key INTEGER NOT NULL,

    source_run_id INTEGER NOT NULL,
    fetched_at TEXT NOT NULL,

    temperature_2m REAL,
    relative_humidity_2m REAL,
    precipitation REAL,
    wind_speed_10m REAL,

    FOREIGN KEY (location_key)
        REFERENCES dim_location(location_key),

    FOREIGN KEY (date_key)
        REFERENCES dim_date(date_key),

    FOREIGN KEY (time_key)
        REFERENCES dim_time(time_key),

    FOREIGN KEY (source_run_id)
        REFERENCES ingestion_runs(run_id),

    UNIQUE(location_key, date_key, time_key, source_run_id)
);

-- Indexes for faster analytical queries
CREATE INDEX IF NOT EXISTS idx_fact_location
ON fact_weather(location_key);

CREATE INDEX IF NOT EXISTS idx_fact_date
ON fact_weather(date_key);

CREATE INDEX IF NOT EXISTS idx_fact_time
ON fact_weather(time_key);

CREATE INDEX IF NOT EXISTS idx_fact_run
ON fact_weather(source_run_id);
