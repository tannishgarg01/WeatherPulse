
import sqlite3
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "weatherpulse.db"


def load_dimensions():

    connection = sqlite3.connect(DB_PATH)

    try:
        connection.execute("PRAGMA foreign_keys = ON")
        cursor = connection.cursor()

        # --------------------------------
        # 1. Load Location Dimension
        # --------------------------------

        cursor.execute("""
            SELECT city_name, latitude, longitude, timezone, country
            FROM locations
        """)

        locations = cursor.fetchall()

        cursor.executemany("""
            INSERT INTO dim_location
            (city_name, latitude, longitude, timezone, country)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(city_name) DO NOTHING
        """, locations)

        # --------------------------------
        # 2. Load Date and Time Dimensions
        # --------------------------------

        cursor.execute("""
            SELECT DISTINCT forecast_time
            FROM weather_forecasts
        """)

        timestamps = cursor.fetchall()

        dates = {}
        times = {}

        for (timestamp,) in timestamps:

            dt = datetime.fromisoformat(timestamp)

            # Date dimension
            date_key = int(dt.strftime("%Y%m%d"))

            dates[date_key] = (
                date_key,
                dt.date().isoformat(),
                dt.day,
                dt.month,
                dt.strftime("%B"),
                dt.year,
                dt.strftime("%A")
            )

            # Time dimension
            time_key = dt.hour * 100 + dt.minute

            if dt.hour < 12:
                period = "Morning"
            elif dt.hour < 17:
                period = "Afternoon"
            elif dt.hour < 21:
                period = "Evening"
            else:
                period = "Night"

            times[time_key] = (
                time_key,
                dt.hour,
                dt.minute,
                period
            )

        cursor.executemany("""
            INSERT INTO dim_date
            (date_key, full_date, day, month,
             month_name, year, day_of_week)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(date_key) DO NOTHING
        """, list(dates.values()))

        cursor.executemany("""
            INSERT INTO dim_time
            (time_key, hour, minute, time_period)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(time_key) DO NOTHING
        """, list(times.values()))

        connection.commit()

        # --------------------------------
        # 3. Verify Dimensions
        # --------------------------------

        for table in ["dim_location", "dim_date", "dim_time"]:

            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]

            print(f"{table}: {count} records")

        print("\nDATE DIMENSION SAMPLE:")

        cursor.execute("""
            SELECT * FROM dim_date
            ORDER BY date_key
            LIMIT 5
        """)

        for row in cursor.fetchall():
            print(row)

        print("\nTIME DIMENSION SAMPLE:")

        cursor.execute("""
            SELECT * FROM dim_time
            ORDER BY time_key
            LIMIT 5
        """)

        for row in cursor.fetchall():
            print(row)

        print("\nDIMENSIONS LOADED SUCCESSFULLY!")

    except (sqlite3.Error, ValueError) as error:
        connection.rollback()
        print("ERROR:", error)

    finally:
        connection.close()
        print("\nDatabase connection closed.")


if __name__ == "__main__":
    load_dimensions()
