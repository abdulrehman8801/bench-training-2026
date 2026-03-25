import json
import sys
from typing import Any, Dict, Optional, Tuple
import requests

WEATHER_CODES = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Drizzle: Light",
    53: "Drizzle: Moderate",
    55: "Drizzle: Dense intensity",
    56: "Freezing Drizzle: Light",
    57: "Freezing Drizzle: Dense intensity",
    61: "Rain: Slight",
    63: "Rain: Moderate",
    65: "Rain: Heavy intensity",
    66: "Freezing Rain: Light",
    67: "Freezing Rain: Heavy intensity",
    71: "Snow fall: Slight",
    73: "Snow fall: Moderate",
    75: "Snow fall: Heavy intensity",
    77: "Snow grains",
    80: "Rain showers: Slight",
    81: "Rain showers: Moderate",
    82: "Rain showers: Violent",
    85: "Snow showers: Slight",
    86: "Snow showers: Heavy",
    95: "Thunderstorm: Slight or moderate",
    96: "Thunderstorm with slight hail",
    99: "Thunderstorm with heavy hail"
}


def _request_json(url: str, timeout_s: int = 20) -> Dict[str, Any]:
    resp = requests.get(url, timeout=timeout_s)
    resp.raise_for_status()
    return resp.json()

def geocode_city(city_name: str) -> Tuple[str, float, float]:
    city_name = city_name.strip()
    if not city_name:
        raise ValueError("city_name cannot be empty")

    geocode_url = (
        "https://geocoding-api.open-meteo.com/v1/search"
        f"?name={requests.utils.quote(city_name)}&count=1&language=en&format=json"
    )
    geocode_json = _request_json(geocode_url)

    print("Raw geocoding JSON:")
    print(json.dumps(geocode_json, indent=2))

    results = geocode_json.get("results") or []
    if not results:
        raise LookupError(f"No coordinates found for city: {city_name}")

    first = results[0]
    return first["name"], float(first["latitude"]), float(first["longitude"])

def fetch_current_weather(latitude: float, longitude: float) -> Dict[str, Any]:
    weather_url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={latitude}&longitude={longitude}&current_weather=true"
    )
    weather_json = _request_json(weather_url)

    print("\nRaw weather JSON:")
    print(json.dumps(weather_json, indent=2))

    current = weather_json.get("current_weather")
    if not current:
        raise LookupError("weather response missing 'current_weather'")
    return current

def main(argv: Optional[list] = None) -> None:
    argv = sys.argv if argv is None else argv
    if len(argv) < 2:
        print("Usage: python exercise_2.py <city_name>", file=sys.stderr)
        sys.exit(1)

    city_input = argv[1]
    try:
        city, lat, lon = geocode_city(city_input)
        current = fetch_current_weather(lat, lon)
    except requests.exceptions.RequestException as exc:
        print(f"Error: network/API request failed: {exc}", file=sys.stderr)
        sys.exit(1)
    except (ValueError, LookupError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    temp_c = current.get("temperature")
    wind_speed = current.get("windspeed")
    weather_code = current.get("weathercode")
    desc = WEATHER_CODES.get(weather_code, f"Unknown (code {weather_code})")

    temp_f = temp_c * 9 / 5 + 32 if temp_c is not None else None

    print(f"\ncity: {city}")
    print(f"temperature (C): {temp_c}°C")
    if temp_f is not None:
        print(f"temperature (F): {temp_f:.2f}°F")
    else:
        print("temperature (F): N/A")
    print(f"wind_speed: {wind_speed}")
    print(f"weather_description: {desc}")

if __name__ == "__main__":
    main()