
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "weatherpulse.db"
SQL_PATH = BASE_DIR / "sql" / "create_gold_layer.sql"


def create_gold_layer():

    if not DB_PATH.exists():
        print("ERROR: Database not found!")
        return

    if not SQL_PATH.exists():
        print("ERROR: Gold Layer SQL file not found!")
        return

    connection = sqlite3.connect(DB_PATH)

    try:
        # Read SQL script
        sql_script = SQL_PATH.read_text(encoding="utf-8")

        # Execute Gold Layer views
        connection.executescript(sql_script)

        cursor = connection.cursor()

        # Verify created views
        cursor.execute("""
            SELECT name
            FROM sqlite_master
            WHERE type = 'view'
            AND name LIKE 'gold_%'
            ORDER BY name
        """)

        views = cursor.fetchall()

        print("\nGOLD LAYER CREATED SUCCESSFULLY")
        print("-" * 40)

        for view in views:
            print(view[0])

        print(f"\nTotal Gold Layer views: {len(views)}")

        connection.commit()

    except sqlite3.Error as error:
        connection.rollback()
        print("DATABASE ERROR:", error)

    finally:
        connection.close()
        print("\nDatabase connection closed.")


if __name__ == "__main__":
    create_gold_layer()
