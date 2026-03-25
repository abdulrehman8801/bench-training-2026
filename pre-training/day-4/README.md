# Day-4

## for exercise_1

username: abdulrehman8801
bio: None
public repos count: 1
followers: 0
top 5 repos by stars:
  repo_name: bench-training-2026
  repo_stars: 0
  repo_language: Python

## for exercise_2

Raw geocoding JSON:
{
  "results": [
    {
      "id": 1172451,
      "name": "Lahore",
      "latitude": 31.558,
      "longitude": 74.35071,
      "elevation": 216.0,
      "feature_code": "PPLA",
      "country_code": "PK",
      "admin1_id": 1167710,
      "admin2_id": 1172449,
      "timezone": "Asia/Karachi",
      "population": 13004135,
      "country_id": 1168579,
      "country": "Pakistan",
      "admin1": "Punjab",
      "admin2": "Lahore"
    }
  ],
  "generationtime_ms": 0.3758669
}

Raw weather JSON:
{
  "latitude": 31.5,
  "longitude": 74.375,
  "generationtime_ms": 0.049948692321777344,
  "utc_offset_seconds": 0,
  "timezone": "GMT",
  "timezone_abbreviation": "GMT",
  "elevation": 219.0,
  "current_weather_units": {
    "time": "iso8601",
    "interval": "seconds",
    "temperature": "°C",
    "windspeed": "km/h",
    "winddirection": "°",
    "is_day": "",
    "weathercode": "wmo code"
  },
  "current_weather": {
    "time": "2026-03-25T09:45",
    "interval": 900,
    "temperature": 29.2,
    "windspeed": 11.7,
    "winddirection": 252,
    "is_day": 1,
    "weathercode": 3
  }
}

city: Lahore
temperature (C): 29.2°C
temperature (F): 84.56°F
wind_speed: 11.7
weather_description: Overcast

The hardest part was reading the API response structure (where each field lives) and then safely extracting only the values I needed.
