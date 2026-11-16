
import sqlite3
from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "weatherpulse.db"
SQL_PATH = BASE_DIR / "sql" / "create_star_schema.sql"


def create_star_schema():

    if not DB_PATH.exists():
        print("ERROR: Database not found!")
        return

    if not SQL_PATH.exists():
        print("ERROR: Star Schema SQL file not found!")
        return

    connection = sqlite3.connect(DB_PATH)

    try:
        # Enable foreign key support
        connection.execute("PRAGMA foreign_keys = ON")

        # Read SQL file
        sql_script = SQL_PATH.read_text(encoding="utf-8")

        # Execute all CREATE TABLE and CREATE INDEX statements
        connection.executescript(sql_script)

        # Verify created tables
        cursor = connection.cursor()

        cursor.execute("""
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
            AND name LIKE 'dim_%' OR name = 'fact_weather'
            ORDER BY name
        """)

        tables = cursor.fetchall()

        print("\nSTAR SCHEMA TABLES CREATED")
        print("-" * 35)

        for table in tables:
            print(table[0])

        print(f"\nTotal Star Schema tables: {len(tables)}")

        connection.commit()

    except sqlite3.Error as error:
        connection.rollback()
        print(f"Database Error: {error}")

    finally:
        connection.close()
        print("\nDatabase connection closed.")


if __name__ == "__main__":
    create_star_schema()
