
import json
from pathlib import Path

# -----------------------------------
# 1. PROJECT PATH
# -----------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]
LANDING_ZONE = PROJECT_ROOT / "landing_zone"

# -----------------------------------
# 2. REQUIRED WEATHER FIELDS
# -----------------------------------

REQUIRED_FIELDS = [
    "time",
    "temperature_2m",
    "relative_humidity_2m",
    "precipitation",
    "wind_speed_10m"
]

EXPECTED_RECORDS = 168


# -----------------------------------
# 3. VALIDATE ONE JSON FILE
# -----------------------------------

def validate_file(file_path):

    print(f"\nChecking: {file_path.name}")

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        hourly_data = data.get("hourly", {})

        # Check required fields
        missing_fields = [
            field for field in REQUIRED_FIELDS
            if field not in hourly_data
        ]

        if missing_fields:
            print("FAILED: Missing fields:", missing_fields)
            return False

        # Check array lengths
        lengths = {
            field: len(hourly_data[field])
            for field in REQUIRED_FIELDS
        }

        if len(set(lengths.values())) != 1:
            print("FAILED: Array lengths do not match:", lengths)
            return False

        record_count = lengths["time"]

        if record_count != EXPECTED_RECORDS:
            print(
                f"FAILED: Expected {EXPECTED_RECORDS} records, "
                f"found {record_count}"
            )
            return False

        # Check missing values
        for field in REQUIRED_FIELDS:
            if any(value is None for value in hourly_data[field]):
                print(f"FAILED: Missing values found in {field}")
                return False

        print(f"SUCCESS: {record_count} hourly records validated.")
        return True

    except (json.JSONDecodeError, OSError, TypeError) as error:
        print("FAILED:", error)
        return False


# -----------------------------------
# 4. VALIDATE ALL CITY FILES
# -----------------------------------

def main():

    print("=" * 45)
    print("WEATHERPULSE DATA VALIDATION")
    print("=" * 45)

    json_files = sorted(LANDING_ZONE.glob("*.json"))

    if not json_files:
        print("No JSON files found!")
        return

    successful = 0
    failed = 0

    for file_path in json_files:

        if validate_file(file_path):
            successful += 1
        else:
            failed += 1

    print("\n" + "=" * 45)
    print("VALIDATION SUMMARY")
    print("=" * 45)

    print(f"Total files: {len(json_files)}")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")


if __name__ == "__main__":
    main()
