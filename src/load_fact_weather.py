
import sqlite3
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "weatherpulse.db"


def load_fact_weather():

    connection = sqlite3.connect(DB_PATH)

    try:
        connection.execute("PRAGMA foreign_keys = ON")
        cursor = connection.cursor()

        # Fetch normalized weather records
        cursor.execute("""
            SELECT
                w.location_id,
                w.run_id,
                w.forecast_time,
                w.fetched_at,
                w.temperature_2m,
                w.relative_humidity_2m,
                w.precipitation,
                w.wind_speed_10m
            FROM weather_forecasts w
        """)

        records = cursor.fetchall()
        fact_records = []

        for record in records:

            (
                location_id,
                run_id,
                forecast_time,
                fetched_at,
                temperature,
                humidity,
                precipitation,
                wind_speed
            ) = record

            dt = datetime.fromisoformat(forecast_time)

            # Get dimension keys
            date_key = int(dt.strftime("%Y%m%d"))
            time_key = dt.hour * 100 + dt.minute

            fact_records.append((
                location_id,
                date_key,
                time_key,
                run_id,
                fetched_at,
                temperature,
                humidity,
                precipitation,
                wind_speed
            ))

        # Insert records into Fact Table
        cursor.executemany("""
            INSERT INTO fact_weather (
                location_key,
                date_key,
                time_key,
                source_run_id,
                fetched_at,
                temperature_2m,
                relative_humidity_2m,
                precipitation,
                wind_speed_10m
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(
                location_key,
                date_key,
                time_key,
                source_run_id
            ) DO NOTHING
        """, fact_records)

        connection.commit()

        # Verify total records
        cursor.execute("SELECT COUNT(*) FROM fact_weather")
        total = cursor.fetchone()[0]

        print("\nFACT WEATHER LOADING COMPLETED")
        print("-" * 40)
        print(f"Source records: {len(records)}")
        print(f"Fact table records: {total}")

        # City-wise record count
        cursor.execute("""
            SELECT
                l.city_name,
                COUNT(f.weather_key)
            FROM fact_weather f
            JOIN dim_location l
                ON f.location_key = l.location_key
            GROUP BY l.city_name
            ORDER BY l.city_name
        """)

        print("\nCITY-WISE FACT RECORDS:")

        for row in cursor.fetchall():
            print(row)

        print("\nFACT TABLE SAMPLE:")

        cursor.execute("""
            SELECT
                l.city_name,
                d.full_date,
                t.hour,
                f.temperature_2m,
                f.relative_humidity_2m
            FROM fact_weather f
            JOIN dim_location l
                ON f.location_key = l.location_key
            JOIN dim_date d
                ON f.date_key = d.date_key
            JOIN dim_time t
                ON f.time_key = t.time_key
            LIMIT 5
        """)

        for row in cursor.fetchall():
            print(row)

        print("\nSTAR SCHEMA FACT TABLE LOADED SUCCESSFULLY!")

    except sqlite3.Error as error:
        connection.rollback()
        print("DATABASE ERROR:", error)

    finally:
        connection.close()
        print("\nDatabase connection closed.")


if __name__ == "__main__":
    load_fact_weather()
