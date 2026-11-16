
# WeatherPulse - Star Schema Design

## 1. Introduction

WeatherPulse uses a Star Schema data warehouse model
for analytical reporting and dashboard generation.

The Star Schema contains one central Fact Table
connected to three Dimension Tables.

## 2. Fact Table

### fact_weather

Stores measurable weather observations.

Columns:
- weather_key (Primary Key)
- location_key (Foreign Key)
- date_key (Foreign Key)
- time_key (Foreign Key)
- temperature_2m
- relative_humidity_2m
- precipitation
- wind_speed_10m

## 3. Dimension Tables

### dim_location

Stores city-related information.

Columns:
- location_key (Primary Key)
- city_name
- latitude
- longitude
- timezone
- country

### dim_date

Stores calendar-related information.

Columns:
- date_key (Primary Key)
- full_date
- day
- month
- month_name
- year
- day_of_week

### dim_time

Stores time-related information.

Columns:
- time_key (Primary Key)
- hour
- minute
- time_period

## 4. Relationships

- dim_location (1) -> (Many) fact_weather
- dim_date (1) -> (Many) fact_weather
- dim_time (1) -> (Many) fact_weather

## 5. Benefits

- Faster analytical queries.
- Easy city-wise weather comparison.
- Monthly and daily weather analysis.
- Simplified dashboard reporting.
- Better organization of analytical data.

## 6. Data Flow

Raw JSON
    |
    v
Bronze Layer
    |
    v
Silver Layer
    |
    v
Star Schema / Gold Layer
    |
    v
WeatherPulse Dashboard
