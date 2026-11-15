
import sqlite3
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DB_FILE = PROJECT_ROOT / "weatherpulse.db"

connection = sqlite3.connect(DB_FILE)

try:
    connection.execute("PRAGMA foreign_keys = ON")

    # Fetch an existing forecast record
    record = connection.execute("""
        SELECT
            location_id,
            run_id,
            forecast_time,
            temperature_2m,
            relative_humidity_2m,
            precipitation,
            wind_speed_10m,
            fetched_at
        FROM weather_forecasts
        LIMIT 1
    """).fetchone()

    if record is None:
        print("No weather record available for testing.")

    else:
        before_count = connection.execute("""
            SELECT COUNT(*) FROM weather_forecasts
        """).fetchone()[0]

        print("Records before test:", before_count)

        try:
            connection.execute("""
                INSERT INTO weather_forecasts (
                    location_id,
                    run_id,
                    forecast_time,
                    temperature_2m,
                    relative_humidity_2m,
                    precipitation,
                    wind_speed_10m,
                    fetched_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, record)

            connection.commit()
            print("WARNING: Duplicate was inserted!")

        except sqlite3.IntegrityError as error:
            connection.rollback()
            print("SUCCESS: Duplicate rejected by database.")
            print("Reason:", error)

        after_count = connection.execute("""
            SELECT COUNT(*) FROM weather_forecasts
        """).fetchone()[0]

        print("Records after test:", after_count)

finally:
    connection.close()
