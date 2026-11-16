
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "weatherpulse.db"
SQL_PATH = BASE_DIR / "sql" / "star_schema_queries.sql"


def run_analysis():

    if not DB_PATH.exists():
        print("ERROR: Database not found!")
        return

    if not SQL_PATH.exists():
        print("ERROR: SQL file not found!")
        return

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    try:
        sql_content = SQL_PATH.read_text(encoding="utf-8")

        # Split SQL file into individual queries
        queries = [
            query.strip()
            for query in sql_content.split(";")
            if query.strip() and "SELECT" in query.upper()
        ]

        print("\nWEATHERPULSE STAR SCHEMA ANALYSIS")
        print("=" * 60)

        for index, query in enumerate(queries, start=1):

            print(f"\nANALYSIS {index}")
            print("-" * 60)

            cursor.execute(query)

            columns = [
                description[0]
                for description in cursor.description
            ]

            print(" | ".join(columns))
            print("-" * 60)

            rows = cursor.fetchall()

            for row in rows:
                print(" | ".join(str(value) for value in row))

            print(f"\nTotal records: {len(rows)}")

        print("\nALL STAR SCHEMA QUERIES EXECUTED SUCCESSFULLY!")

    except sqlite3.Error as error:
        print("SQL ERROR:", error)

    finally:
        connection.close()
        print("\nDatabase connection closed.")


if __name__ == "__main__":
    run_analysis()