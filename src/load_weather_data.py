
import json
import sqlite3
from pathlib import Path
from datetime import datetime, timezone


# -----------------------------------------
# 1. PROJECT PATHS
# -----------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

LANDING_ZONE = PROJECT_ROOT / "landing_zone"
DB_FILE = PROJECT_ROOT / "weatherpulse.db"


# -----------------------------------------
# 2. LOAD WEATHER DATA
# -----------------------------------------

def load_weather_data():

    connection = sqlite3.connect(DB_FILE)
    connection.execute("PRAGMA foreign_keys = ON")

    successful_files = 0
    failed_files = 0
    total_records = 0

    # Unique ingestion run for this execution
    started_at = datetime.now(timezone.utc).isoformat()

    try:

        print("=" * 50)
        print("WEATHERPULSE DATABASE LOADER")
        print("=" * 50)

        # -----------------------------------------
        # Create ingestion run
        # -----------------------------------------

        cursor = connection.execute("""
            INSERT INTO ingestion_runs (
                started_at,
                status,
                total_locations,
                successful_locations,
                failed_locations
            )
            VALUES (?, 'FAILED', 0, 0, 0)
        """, (started_at,))

        run_id = cursor.lastrowid

        # Get all JSON files
        json_files = sorted(LANDING_ZONE.glob("*.json"))

        if not json_files:
            raise FileNotFoundError("No JSON files found!")

        for file_path in json_files:

            print(f"\nProcessing: {file_path.name}")

            try:

                with open(file_path, "r", encoding="utf-8") as file:
                    data = json.load(file)

                # Extract city name from filename
                city_name = file_path.name.split("_")[0].title()

                # Find location ID
                location = connection.execute("""
                    SELECT location_id
                    FROM locations
                    WHERE city_name = ?
                """, (city_name,)).fetchone()

                if location is None:
                    raise ValueError(f"Location not found: {city_name}")

                location_id = location[0]

                hourly = data["hourly"]

                times = hourly["time"]
                temperatures = hourly["temperature_2m"]
                humidities = hourly["relative_humidity_2m"]
                precipitation = hourly["precipitation"]
                wind_speeds = hourly["wind_speed_10m"]

                arrays = [
                    times,
                    temperatures,
                    humidities,
                    precipitation,
                    wind_speeds
                ]

                # Ensure all arrays have equal length
                if len({len(arr) for arr in arrays}) != 1:
                    raise ValueError("Hourly array lengths do not match")

                fetched_at = datetime.now(timezone.utc).isoformat()

                records = []

                for i in range(len(times)):

                    records.append((
                        location_id,
                        run_id,
                        times[i],
                        temperatures[i],
                        humidities[i],
                        precipitation[i],
                        wind_speeds[i],
                        fetched_at
                    ))

                # Insert hourly records
                connection.executemany("""
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
                """, records)

                connection.commit()

                total_records += len(records)
                successful_files += 1

                print(f"SUCCESS: {len(records)} records inserted.")

            except (ValueError, KeyError, OSError, sqlite3.Error) as error:

                connection.rollback()
                failed_files += 1

                print(f"FAILED: {city_name if 'city_name' in locals() else file_path.name}")
                print("Reason:", error)

        # -----------------------------------------
        # Update ingestion run
        # -----------------------------------------

        if failed_files == 0:
            status = "SUCCESS"
        elif successful_files > 0:
            status = "PARTIAL"
        else:
            status = "FAILED"

        completed_at = datetime.now(timezone.utc).isoformat()

        connection.execute("""
            UPDATE ingestion_runs
            SET completed_at = ?,
                status = ?,
                total_locations = ?,
                successful_locations = ?,
                failed_locations = ?
            WHERE run_id = ?
        """, (
            completed_at,
            status,
            len(json_files),
            successful_files,
            failed_files,
            run_id
        ))

        connection.commit()

        print("\n" + "=" * 50)
        print("DATABASE LOADING SUMMARY")
        print("=" * 50)

        print("Run ID:", run_id)
        print("Status:", status)
        print("Total files:", len(json_files))
        print("Successful:", successful_files)
        print("Failed:", failed_files)
        print("Total records inserted:", total_records)

    except (OSError, sqlite3.Error, ValueError) as error:

        connection.rollback()
        print("\nDATABASE LOADING ERROR:", error)

    finally:
        connection.close()


# -----------------------------------------
# 3. RUN PIPELINE
# -----------------------------------------

if __name__ == "__main__":
    load_weather_data()
