
import sqlite3
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware


# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "weatherpulse.db"


# Initialize FastAPI
app = FastAPI(
    title="WeatherPulse API",
    description="Weather analytics API powered by SQLite Gold Layer",
    version="1.0.0"
)


# Allow React frontend to access backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Database connection
def get_connection():

    if not DB_PATH.exists():
        raise HTTPException(
            status_code=500,
            detail="WeatherPulse database not found"
        )

    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row

    return connection


# Convert database rows to JSON-friendly dictionaries
def fetch_data(query):

    connection = get_connection()

    try:
        cursor = connection.cursor()
        cursor.execute(query)

        return [dict(row) for row in cursor.fetchall()]

    except sqlite3.Error as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )

    finally:
        connection.close()


# 1. Health Check
@app.get("/api/health")
def health_check():

    return {
        "status": "healthy",
        "application": "WeatherPulse",
        "database": "SQLite"
    }


# 2. City-wise Weather Summary
@app.get("/api/weather/summary")
def weather_summary():

    return fetch_data("""
        SELECT *
        FROM gold_city_weather_summary
        ORDER BY avg_temperature DESC
    """)


# 3. Daily Weather Trends
@app.get("/api/weather/daily")
def daily_weather():

    return fetch_data("""
        SELECT *
        FROM gold_daily_weather_trend
        ORDER BY full_date
    """)


# 4. Hourly Weather Trends
@app.get("/api/weather/hourly")
def hourly_weather():

    return fetch_data("""
        SELECT *
        FROM gold_hourly_weather_trend
        ORDER BY hour
    """)


# 5. Dashboard KPI Statistics
@app.get("/api/weather/kpis")
def weather_kpis():

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                ROUND(AVG(avg_temperature), 2)
                    AS average_temperature,

                ROUND(AVG(avg_humidity), 2)
                    AS average_humidity,

                ROUND(SUM(total_precipitation), 2)
                    AS total_precipitation,

                MAX(max_wind_speed)
                    AS maximum_wind_speed

            FROM gold_city_weather_summary
        """)

        return dict(cursor.fetchone())

    except sqlite3.Error as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )

    finally:
        connection.close()