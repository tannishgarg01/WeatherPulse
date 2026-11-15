
import sqlite3
from pathlib import Path

# -----------------------------------
# 1. PROJECT PATHS
# -----------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

SQL_FILE = PROJECT_ROOT / "sql" / "create_tables.sql"
DB_FILE = PROJECT_ROOT / "weatherpulse.db"


# -----------------------------------
# 2. CREATE DATABASE
# -----------------------------------

def create_database():

    print("=" * 45)
    print("WEATHERPULSE DATABASE SETUP")
    print("=" * 45)

    if not SQL_FILE.exists():
        print("ERROR: create_tables.sql not found!")
        return

    try:
        connection = sqlite3.connect(DB_FILE)

        # Enable foreign key constraints
        connection.execute("PRAGMA foreign_keys = ON")

        # Read SQL file
        with open(SQL_FILE, "r", encoding="utf-8") as file:
            sql_script = file.read()

        # Execute table creation commands
        connection.executescript(sql_script)

        connection.commit()

        # Verify created tables
        cursor = connection.cursor()

        cursor.execute("""
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
            AND name NOT LIKE 'sqlite_%'
            ORDER BY name;
        """)

        tables = cursor.fetchall()

        print("\nDatabase created successfully!")
        print(f"Database file: {DB_FILE.name}")

        print("\nTables created:")

        for table in tables:
            print(f"SUCCESS: {table[0]}")

        print(f"\nTotal tables: {len(tables)}")

        connection.close()

    except sqlite3.Error as error:
        print("DATABASE ERROR:", error)


# -----------------------------------
# 3. RUN DATABASE SETUP
# -----------------------------------

if __name__ == "__main__":
    create_database()
