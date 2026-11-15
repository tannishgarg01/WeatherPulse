
import sqlite3
from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "weatherpulse.db"
SQL_PATH = BASE_DIR / "sql" / "analysis_queries.sql"


def run_analysis():
    if not DB_PATH.exists():
        print("ERROR: Database file not found!")
        return

    if not SQL_PATH.exists():
        print("ERROR: SQL analysis file not found!")
        return

    # Read SQL queries
    sql_content = SQL_PATH.read_text(encoding="utf-8")
    queries = [
        query.strip()
        for query in sql_content.split(";")
        if query.strip() and "SELECT" in query.upper()
    ]

    # Connect to database
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    try:
        for index, query in enumerate(queries, start=1):
            print("\n" + "=" * 55)
            print(f"ANALYSIS {index}")
            print("=" * 55)

            cursor.execute(query)

            # Display column names
            columns = [description[0] for description in cursor.description]
            print(" | ".join(columns))
            print("-" * 55)

            # Display results
            rows = cursor.fetchall()

            for row in rows:
                print(" | ".join(str(value) for value in row))

            print(f"\nTotal records: {len(rows)}")

    except sqlite3.Error as error:
        print(f"SQL ERROR: {error}")

    finally:
        connection.close()
        print("\nDatabase connection closed.")


if __name__ == "__main__":
    run_analysis()
