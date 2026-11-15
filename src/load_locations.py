
import sqlite3
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DB_FILE = PROJECT_ROOT / "weatherpulse.db"

CITIES = [
    ("Delhi", 28.576448, 77.186780, "Asia/Kolkata", "India"),
    ("Mumbai", 19.0760, 72.8777, "Asia/Kolkata", "India"),
    ("Chandigarh", 30.7333, 76.7794, "Asia/Kolkata", "India"),
    ("Bengaluru", 12.9716, 77.5946, "Asia/Kolkata", "India"),
    ("Ludhiana", 30.9010, 75.8573, "Asia/Kolkata", "India"),
    ("Patiala", 30.3398, 76.3869, "Asia/Kolkata", "India"),
    ("Chennai", 13.0827, 80.2707, "Asia/Kolkata", "India")
]

def load_locations():

    connection = sqlite3.connect(DB_FILE)

    try:
        connection.execute("PRAGMA foreign_keys = ON")

        connection.executemany("""
            INSERT INTO locations
            (city_name, latitude, longitude, timezone, country)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(city_name) DO NOTHING
        """, CITIES)

        connection.commit()

        cursor = connection.execute("""
            SELECT location_id, city_name, latitude, longitude
            FROM locations
            ORDER BY location_id
        """)

        print("\nWEATHERPULSE LOCATIONS")
        print("-" * 55)

        for row in cursor.fetchall():
            print(row)

        print("\nTotal locations:", connection.execute(
            "SELECT COUNT(*) FROM locations"
        ).fetchone()[0])

    finally:
        connection.close()


if __name__ == "__main__":
    load_locations()
