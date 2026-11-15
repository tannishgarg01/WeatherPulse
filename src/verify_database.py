
import sqlite3
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DB_FILE = PROJECT_ROOT / "weatherpulse.db"

connection = sqlite3.connect(DB_FILE)

print("=" * 50)
print("WEATHERPULSE DATABASE VERIFICATION")
print("=" * 50)

# 1. Count records in all tables
for table in ["locations", "ingestion_runs", "weather_forecasts"]:

    count = connection.execute(
        f"SELECT COUNT(*) FROM {table}"
    ).fetchone()[0]

    print(f"{table}: {count} records")


# 2. Records city-wise
print("\nCITY-WISE WEATHER RECORDS")
print("-" * 50)

query = """
SELECT
    l.city_name,
    COUNT(w.forecast_id) AS total_records
FROM locations l
LEFT JOIN weather_forecasts w
    ON l.location_id = w.location_id
GROUP BY l.location_id, l.city_name
ORDER BY l.city_name;
"""

for row in connection.execute(query):
    print(row)


# 3. Latest ingestion run
print("\nINGESTION RUN HISTORY")
print("-" * 50)

query = """
SELECT
    run_id,
    status,
    total_locations,
    successful_locations,
    failed_locations
FROM ingestion_runs;
"""

for row in connection.execute(query):
    print(row)


# 4. Sample weather records
print("\nSAMPLE WEATHER RECORDS")
print("-" * 50)

query = """
SELECT
    l.city_name,
    w.forecast_time,
    w.temperature_2m,
    w.relative_humidity_2m,
    w.precipitation,
    w.wind_speed_10m
FROM weather_forecasts w
JOIN locations l
    ON w.location_id = l.location_id
ORDER BY w.forecast_id
LIMIT 5;
"""

for row in connection.execute(query):
    print(row)


# 5. Foreign key validation
print("\nFOREIGN KEY CHECK")
print("-" * 50)

errors = connection.execute(
    "PRAGMA foreign_key_check"
).fetchall()

print("Foreign key errors:", len(errors))

connection.close()

print("\nDATABASE VERIFICATION COMPLETED!")
