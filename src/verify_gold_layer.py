
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "weatherpulse.db"


def verify_gold_layer():

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    views = [
        "gold_city_weather_summary",
        "gold_daily_weather_trend",
        "gold_hourly_weather_trend"
    ]

    try:
        print("\nGOLD LAYER VERIFICATION")
        print("=" * 55)

        for view in views:

            print(f"\nVIEW: {view}")
            print("-" * 55)

            cursor.execute(f"SELECT * FROM {view}")
            rows = cursor.fetchall()

            columns = [
                description[0]
                for description in cursor.description
            ]

            print(" | ".join(columns))
            print("-" * 55)

            for row in rows:
                print(" | ".join(str(value) for value in row))

            print(f"\nTotal records: {len(rows)}")

        print("\nALL GOLD LAYER VIEWS VERIFIED SUCCESSFULLY!")

    except sqlite3.Error as error:
        print("DATABASE ERROR:", error)

    finally:
        connection.close()
        print("\nDatabase connection closed.")


if __name__ == "__main__":
    verify_gold_layer()
