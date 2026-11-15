
-- ==========================================
-- WEATHERPULSE DATABASE
-- Normalized Relational Schema (3NF)
-- Database: SQLite
-- ==========================================

PRAGMA foreign_keys = ON;

-- ==========================================
-- 1. LOCATIONS TABLE
-- ==========================================

CREATE TABLE IF NOT EXISTS locations (
    location_id INTEGER PRIMARY KEY AUTOINCREMENT,
    city_name TEXT NOT NULL UNIQUE,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL,
    timezone TEXT NOT NULL,
    country TEXT NOT NULL
);

-- ==========================================
-- 2. INGESTION RUNS TABLE
-- ==========================================

CREATE TABLE IF NOT EXISTS ingestion_runs (
    run_id INTEGER PRIMARY KEY AUTOINCREMENT,
    started_at TEXT NOT NULL,
    completed_at TEXT,
    status TEXT NOT NULL
        CHECK (status IN ('SUCCESS', 'PARTIAL', 'FAILED')),
    total_locations INTEGER NOT NULL DEFAULT 0,
    successful_locations INTEGER NOT NULL DEFAULT 0,
    failed_locations INTEGER NOT NULL DEFAULT 0
);

-- ==========================================
-- 3. WEATHER FORECASTS TABLE
-- ==========================================

CREATE TABLE IF NOT EXISTS weather_forecasts (
    forecast_id INTEGER PRIMARY KEY AUTOINCREMENT,

    location_id INTEGER NOT NULL,
    run_id INTEGER NOT NULL,

    forecast_time TEXT NOT NULL,

    temperature_2m REAL,
    relative_humidity_2m REAL,
    precipitation REAL,
    wind_speed_10m REAL,

    fetched_at TEXT NOT NULL,

    FOREIGN KEY (location_id)
        REFERENCES locations(location_id),

    FOREIGN KEY (run_id)
        REFERENCES ingestion_runs(run_id),

    CHECK (
        relative_humidity_2m IS NULL
        OR relative_humidity_2m BETWEEN 0 AND 100
    ),

    CHECK (
        precipitation IS NULL OR precipitation >= 0
    ),

    CHECK (
        wind_speed_10m IS NULL OR wind_speed_10m >= 0
    ),

    UNIQUE (location_id, forecast_time, fetched_at)
);

-- ==========================================
-- 4. INDEXES FOR FASTER QUERIES
-- ==========================================

CREATE INDEX IF NOT EXISTS idx_weather_location
ON weather_forecasts(location_id);

CREATE INDEX IF NOT EXISTS idx_weather_forecast_time
ON weather_forecasts(forecast_time);

CREATE INDEX IF NOT EXISTS idx_weather_run
ON weather_forecasts(run_id);
