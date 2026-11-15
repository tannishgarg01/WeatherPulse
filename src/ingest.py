import requests
import json
import time
from pathlib import Path
from datetime import datetime, timezone
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


# -----------------------------------------
# 1. API CONFIGURATION
# -----------------------------------------

API_URL = "https://api.open-meteo.com/v1/forecast"

# Seven selected locations
CITIES = {
    "Delhi": {"latitude": 28.6139, "longitude": 77.2090},
    "Mumbai": {"latitude": 19.0760, "longitude": 72.8777},
    "Chandigarh": {"latitude": 30.7333, "longitude": 76.7794},
    "Bengaluru": {"latitude": 12.9716, "longitude": 77.5946},
    "Ludhiana": {"latitude": 30.9010, "longitude": 75.8573},
    "Patiala": {"latitude": 30.3398, "longitude": 76.3869},
    "Chennai": {"latitude": 13.0827, "longitude": 80.2707}
}

# Weather variables to fetch
WEATHER_VARIABLES = [
    "temperature_2m",
    "relative_humidity_2m",
    "precipitation",
    "wind_speed_10m"
]


# -----------------------------------------
# 2. CREATE LANDING ZONE
# -----------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]
LANDING_ZONE = PROJECT_ROOT / "landing_zone"

LANDING_ZONE.mkdir(parents=True, exist_ok=True)


# -----------------------------------------
# 3. CONFIGURE RETRIES AND BACKOFF
# -----------------------------------------

retry_strategy = Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["GET"]
)

adapter = HTTPAdapter(max_retries=retry_strategy)

session = requests.Session()
session.mount("https://", adapter)


# -----------------------------------------
# 4. FETCH WEATHER DATA
# -----------------------------------------

def fetch_weather(city, coordinates):

    params = {
        "latitude": coordinates["latitude"],
        "longitude": coordinates["longitude"],
        "hourly": WEATHER_VARIABLES,
        "forecast_days": 7,
        "timezone": "auto"
    }

    try:
        response = session.get(
            API_URL,
            params=params,
            timeout=30
        )

        response.raise_for_status()

        weather_data = response.json()

        # Save original API response as raw JSON
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

        file_path = LANDING_ZONE / f"{city.lower()}_{timestamp}.json"

        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(weather_data, file, indent=4)

        print(f"SUCCESS: {city} weather data saved.")
        print(f"File: {file_path.name}")

        return True

    except requests.exceptions.RequestException as error:
        print(f"ERROR: Could not fetch data for {city}.")
        print(f"Reason: {error}")

    except (ValueError, OSError) as error:
        print(f"ERROR: Could not process or save {city} data.")
        print(f"Reason: {error}")

    return False


# -----------------------------------------
# 5. MAIN INGESTION PIPELINE
# -----------------------------------------

def main():

    print("Starting WeatherPulse API Ingestion...")
    print("-" * 45)

    successful = 0
    failed = 0

    for city, coordinates in CITIES.items():

        print(f"\nFetching weather for {city}...")

        result = fetch_weather(city, coordinates)

        if result:
            successful += 1
        else:
            failed += 1

        # Small pause between city requests
        time.sleep(1)

    print("\n" + "=" * 45)
    print("WEATHER INGESTION SUMMARY")
    print("=" * 45)
    print(f"Total locations: {len(CITIES)}")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    print(f"Landing zone: {LANDING_ZONE}")


# -----------------------------------------
# 6. RUN PIPELINE
# -----------------------------------------

if __name__ == "__main__":
    main()