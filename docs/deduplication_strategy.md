
# WeatherPulse - Deduplication Strategy

## 1. Objective

The purpose of deduplication is to prevent duplicate
weather forecast snapshots while preserving historical
forecast updates received from the Open-Meteo API.

## 2. Duplicate Identification

WeatherPulse identifies a forecast snapshot using
the following combination:

- location_id
- forecast_time
- fetched_at

These three fields together identify a unique
forecast snapshot.

## 3. Deduplication Scenarios

### Scenario A: Exact Duplicate

If the same location, forecast time and fetched_at
are received again, the record is considered a duplicate.

Action:
- Reject the duplicate record.
- Preserve the original record.

### Scenario B: Updated Forecast

If the same location and forecast_time are received
with a different fetched_at timestamp, it is treated
as a new forecast snapshot.

Action:
- Preserve both records.
- Maintain historical forecast information.

### Scenario C: Different Locations

Forecasts belonging to different locations are
stored independently.

Action:
- Preserve all valid records.

## 4. Database Implementation

The weather_forecasts table implements a UNIQUE
constraint on:

(location_id, forecast_time, fetched_at)

SQL:

```sql
UNIQUE (location_id, forecast_time, fetched_at)
```

This prevents exact duplicate forecast snapshots.

## 5. Historical Data Preservation

WeatherPulse does not overwrite earlier forecast
snapshots when updated forecasts are received.

The fetched_at timestamp helps distinguish between
different API ingestion snapshots.

## 6. Error Handling

If a duplicate record violates the UNIQUE constraint,
the database rejects that insertion.

The ingestion process should handle this database
error without corrupting previously stored records.

## 7. Benefits

- Prevents exact duplicate snapshots.
- Preserves historical forecast changes.
- Maintains data consistency.
- Supports historical weather analysis.
- Makes repeated ingestion safer.
