# src/weather_server.py
"""
Weather MCP Server
Wraps the OpenWeatherMap API to give Claude weather superpowers
"""

from mcp.server.fastmcp import FastMCP
import httpx
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Create the MCP server with a name
mcp = FastMCP("Weather Server 🌤️")

# Get API key from environment variable
API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org"


# ─────────────────────────────────────────────
# TOOL 1: Get Current Weather
# ─────────────────────────────────────────────

@mcp.tool()
async def get_current_weather(city: str, units: str = "metric") -> str:
    """
    Get the current weather conditions for any city in the world.

    Args:
        city: City name — e.g. "London", "New York", "Tokyo", "Paris"
        units: Temperature unit — "metric" for Celsius, "imperial" for Fahrenheit, "standard" for Kelvin
    """
    if not API_KEY:
        return "❌ ERROR: OPENWEATHER_API_KEY is not set. Check your .env file."

    unit_symbol = "°C" if units == "metric" else "°F" if units == "imperial" else "K"

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_URL}/data/2.5/weather",
            params={
                "q": city,
                "appid": API_KEY,
                "units": units
            },
            timeout=10.0
        )

    # Handle errors from the API
    if response.status_code == 401:
        return "❌ ERROR: Invalid API key. Check your OPENWEATHER_API_KEY."
    if response.status_code == 404:
        return f"❌ ERROR: City '{city}' not found. Try a different spelling."
    if response.status_code != 200:
        return f"❌ ERROR: API returned status {response.status_code}: {response.text}"

    data = response.json()

    # Extract all the useful info
    name        = data["name"]
    country     = data["sys"]["country"]
    temp        = data["main"]["temp"]
    feels_like  = data["main"]["feels_like"]
    temp_min    = data["main"]["temp_min"]
    temp_max    = data["main"]["temp_max"]
    humidity    = data["main"]["humidity"]
    pressure    = data["main"]["pressure"]
    description = data["weather"][0]["description"].title()
    wind_speed  = data["wind"]["speed"]
    wind_deg    = data["wind"].get("deg", "N/A")
    clouds      = data["clouds"]["all"]
    visibility  = data.get("visibility", "N/A")

    return f"""
╔══════════════════════════════════════╗
  🌍  {name}, {country}
╚══════════════════════════════════════╝

🌤️  Condition:    {description}
🌡️  Temperature:  {temp}{unit_symbol}  (feels like {feels_like}{unit_symbol})
📊  Range:        {temp_min}{unit_symbol} → {temp_max}{unit_symbol}
💧  Humidity:     {humidity}%
🌬️  Pressure:     {pressure} hPa
💨  Wind:         {wind_speed} m/s at {wind_deg}°
☁️  Cloud Cover:  {clouds}%
👁️  Visibility:   {visibility} meters
"""


# ─────────────────────────────────────────────
# TOOL 2: Get 5-Day Forecast
# ─────────────────────────────────────────────

@mcp.tool()
async def get_weather_forecast(city: str, days: int = 5, units: str = "metric") -> str:
    """
    Get a multi-day weather forecast for any city.

    Args:
        city: City name — e.g. "Berlin", "Sydney", "Cairo"
        days: How many days of forecast to show (1 to 5)
        units: Temperature unit — "metric" for Celsius, "imperial" for Fahrenheit
    """
    if not API_KEY:
        return "❌ ERROR: OPENWEATHER_API_KEY is not set. Check your .env file."

    # Clamp days between 1 and 5
    days = max(1, min(5, days))
    unit_symbol = "°C" if units == "metric" else "°F" if units == "imperial" else "K"

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_URL}/data/2.5/forecast",
            params={
                "q": city,
                "appid": API_KEY,
                "units": units,
                "cnt": 40  # Maximum data points (covers 5 days)
            },
            timeout=10.0
        )

    if response.status_code == 401:
        return "❌ ERROR: Invalid API key."
    if response.status_code == 404:
        return f"❌ ERROR: City '{city}' not found."
    if response.status_code != 200:
        return f"❌ ERROR: {response.status_code}: {response.text}"

    data = response.json()
    city_name = data["city"]["name"]
    country   = data["city"]["country"]

    # Group forecast data by day
    daily_data = {}
    for item in data["list"]:
        date = item["dt_txt"].split(" ")[0]  # e.g. "2024-12-25"
        if date not in daily_data:
            daily_data[date] = {
                "temps": [],
                "conditions": [],
                "humidity": [],
                "wind": []
            }
        daily_data[date]["temps"].append(item["main"]["temp"])
        daily_data[date]["conditions"].append(item["weather"][0]["description"])
        daily_data[date]["humidity"].append(item["main"]["humidity"])
        daily_data[date]["wind"].append(item["wind"]["speed"])

    result = f"📅 {days}-Day Forecast — {city_name}, {country}\n"
    result += "═" * 45 + "\n\n"

    for date, info in list(daily_data.items())[:days]:
        temps      = info["temps"]
        conditions = info["conditions"]
        humidity   = info["humidity"]
        wind       = info["wind"]

        # Most common weather condition for the day
        most_common = max(set(conditions), key=conditions.count).title()

        result += f"📆  {date}\n"
        result += f"    🌡️  {min(temps):.1f}{unit_symbol} → {max(temps):.1f}{unit_symbol}\n"
        result += f"    🌤️  {most_common}\n"
        result += f"    💧  Humidity: {sum(humidity)/len(humidity):.0f}%\n"
        result += f"    💨  Wind: {sum(wind)/len(wind):.1f} m/s avg\n"
        result += "\n"

    return result


# ─────────────────────────────────────────────
# TOOL 3: Search Cities
# ─────────────────────────────────────────────

@mcp.tool()
async def search_cities(query: str) -> str:
    """
    Search for cities by name. Useful when you need to find the exact
    city name or distinguish between cities with the same name (e.g. "Springfield").

    Args:
        query: City name to search for — e.g. "Springfield", "Manchester", "Alexandria"
    """
    if not API_KEY:
        return "❌ ERROR: OPENWEATHER_API_KEY is not set."

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_URL}/geo/1.0/direct",
            params={
                "q": query,
                "limit": 5,
                "appid": API_KEY
            },
            timeout=10.0
        )

    if response.status_code != 200:
        return f"❌ ERROR: {response.status_code}: {response.text}"

    cities = response.json()

    if not cities:
        return f"🔍 No cities found matching '{query}'. Try a different spelling."

    result = f"🔍 Cities matching '{query}':\n"
    result += "═" * 40 + "\n\n"

    for i, city in enumerate(cities, 1):
        name    = city.get("name", "Unknown")
        country = city.get("country", "??")
        state   = city.get("state", "")
        lat     = city.get("lat", 0)
        lon     = city.get("lon", 0)

        state_str = f", {state}" if state else ""
        result += f"{i}. {name}{state_str}, {country}\n"
        result += f"   📍 Coordinates: {lat:.4f}°N, {lon:.4f}°E\n\n"

    return result


# ─────────────────────────────────────────────
# Run the server
# ─────────────────────────────────────────────

if __name__ == "__main__":
    print("🚀 Starting Weather MCP Server...")
    print("📡 Waiting for connections...")
    mcp.run()
