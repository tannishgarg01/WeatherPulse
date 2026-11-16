
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "weatherpulse.db"


def verify_star_schema():

    connection = sqlite3.connect(DB_PATH)

    try:
        connection.execute("PRAGMA foreign_keys = ON")
        cursor = connection.cursor()

        print("\nSTAR SCHEMA VERIFICATION")
        print("=" * 45)

        # 1. Table record counts
        tables = [
            "dim_location",
            "dim_date",
            "dim_time",
            "fact_weather"
        ]

        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"{table}: {count} records")

        # 2. City-wise weather summary
        print("\nCITY-WISE WEATHER SUMMARY")
        print("-" * 45)

        cursor.execute("""
            SELECT
                l.city_name,
                ROUND(AVG(f.temperature_2m), 2),
                ROUND(AVG(f.relative_humidity_2m), 2),
                ROUND(SUM(f.precipitation), 2),
                MAX(f.wind_speed_10m),
                COUNT(*)
            FROM fact_weather f
            JOIN dim_location l
                ON f.location_key = l.location_key
            GROUP BY l.city_name
            ORDER BY l.city_name
        """)

        for row in cursor.fetchall():
            print(row)

        # 3. Foreign key verification
        print("\nFOREIGN KEY VERIFICATION")
        cursor.execute("PRAGMA foreign_key_check")
        errors = cursor.fetchall()

        if errors:
            print("Foreign key errors:", errors)
        else:
            print("No foreign key errors found!")

        # 4. Check missing dimension references
        cursor.execute("""
            SELECT COUNT(*)
            FROM fact_weather f
            LEFT JOIN dim_location l
                ON f.location_key = l.location_key
            LEFT JOIN dim_date d
                ON f.date_key = d.date_key
            LEFT JOIN dim_time t
                ON f.time_key = t.time_key
            WHERE l.location_key IS NULL
               OR d.date_key IS NULL
               OR t.time_key IS NULL
        """)

        missing = cursor.fetchone()[0]

        print("\nMISSING DIMENSION REFERENCES:", missing)

        if missing == 0 and not errors:
            print("\nSTAR SCHEMA VERIFIED SUCCESSFULLY!")

    except sqlite3.Error as error:
        print("DATABASE ERROR:", error)

    finally:
        connection.close()
        print("\nDatabase connection closed.")


if __name__ == "__main__":
    verify_star_schema()