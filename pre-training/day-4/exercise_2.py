import requests
import argparse

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

def fetch_current_weather(city_name):
    fetch_coordinates = requests.get(f'https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=1&language=en&format=json')
    coordinates = fetch_coordinates.json()

    city = coordinates["results"][0]["name"]
    latitude = coordinates["results"][0]["latitude"]
    longitude = coordinates["results"][0]["longitude"]

    fetch_weather = requests.get(f'https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true')
    weather = fetch_weather.json()

    print(f'city: {city}')
    print(f'temperature (C): {weather["current_weather"]["temperature"]}°C')
    print(f'temperature (F): {weather["current_weather"]["temperature"] * 9/5 + 32}°F')
    print(f'wind_speed: {weather["current_weather"]["windspeed"]}')
    print(f'weather_description: {WEATHER_CODES[weather["current_weather"]["weathercode"]]}')

def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")

    parser_city_name = subparsers.add_parser("city_name")
    parser_city_name.add_argument("city_name", type=str)

    args = parser.parse_args()
    fetch_current_weather(args.city_name)

if __name__ == "__main__":
    main()