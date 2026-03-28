import requests
from fastmcp import FastMCP
from urllib.parse import quote

mcp = FastMCP("travel-mcp")


@mcp.tool()
def get_weather(city: str) -> str:
    """
    Get current weather for a given city.
    Uses Open-Meteo APIs (no API key required).
    """

    # Step 1: Convert city name to latitude & longitude
    geocode_url = "https://geocoding-api.open-meteo.com/v1/search"

    geo_response = requests.get(
        geocode_url,
        params={
            "name": city,
            "count": 1
        },
        timeout=10
    )

    if geo_response.status_code != 200:
        return "Geocoding service is unavailable."

    geo_data = geo_response.json()

    if "results" not in geo_data or len(geo_data["results"]) == 0:
        return f"City '{city}' was not found."

    latitude = geo_data["results"][0]["latitude"]
    longitude = geo_data["results"][0]["longitude"]

    # Step 2: Fetch current weather
    weather_url = "https://api.open-meteo.com/v1/forecast"

    weather_response = requests.get(
        weather_url,
        params={
            "latitude": latitude,
            "longitude": longitude,
            "current_weather": True
        },
        timeout=10
    )

    if weather_response.status_code != 200:
        return "Weather service is unavailable."

    weather_data = weather_response.json()
    current_weather = weather_data.get("current_weather")

    if not current_weather:
        return "Weather data is not available."

    temperature = current_weather.get("temperature")
    windspeed = current_weather.get("windspeed")

    return (
        f"Current weather in {city}: "
        f"{temperature}°C with wind speed {windspeed} km/h."
    )


if __name__ == "__main__":
    mcp.run(
        transport="http",
        host="0.0.0.0",
        port=8080
    )
