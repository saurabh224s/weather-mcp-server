# test_server.py
"""
Run this script first to make sure everything is working.
It tests each tool directly without needing Claude Desktop.

How to run:
    python test_server.py
"""

import asyncio
import os
from dotenv import load_dotenv
import httpx

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org"


def print_header(title: str):
    print(f"\n{'='*50}")
    print(f"  🧪 {title}")
    print(f"{'='*50}")


async def test_api_key():
    """Test if the API key is valid"""
    print_header("Test 1: Checking API Key")

    if not API_KEY:
        print("❌ FAIL: No API key found!")
        print("   → Make sure you created a .env file")
        print("   → Make sure it contains: OPENWEATHER_API_KEY=your_key_here")
        return False

    print(f"✅ API key found: {API_KEY[:6]}...{API_KEY[-4:]} (hidden for security)")
    return True


async def test_current_weather():
    """Test fetching current weather"""
    print_header("Test 2: Current Weather (London)")

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_URL}/data/2.5/weather",
            params={"q": "London", "appid": API_KEY, "units": "metric"},
            timeout=10.0
        )

    if response.status_code == 401:
        print("❌ FAIL: API key is invalid or not activated yet")
        print("   → Wait 15 minutes after creating your key, then try again")
        return False

    if response.status_code == 200:
        data = response.json()
        temp = data["main"]["temp"]
        desc = data["weather"][0]["description"]
        print(f"✅ SUCCESS!")
        print(f"   London is currently {temp}°C with {desc}")
        return True

    print(f"❌ FAIL: Got status code {response.status_code}")
    print(f"   Response: {response.text}")
    return False


async def test_forecast():
    """Test fetching weather forecast"""
    print_header("Test 3: Weather Forecast (Tokyo)")

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_URL}/data/2.5/forecast",
            params={"q": "Tokyo", "appid": API_KEY, "units": "metric", "cnt": 8},
            timeout=10.0
        )

    if response.status_code == 200:
        data = response.json()
        city = data["city"]["name"]
        count = len(data["list"])
        print(f"✅ SUCCESS!")
        print(f"   Got {count} forecast entries for {city}")
        return True

    print(f"❌ FAIL: Got status code {response.status_code}")
    return False


async def test_city_search():
    """Test city search"""
    print_header("Test 4: City Search (Springfield)")

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_URL}/geo/1.0/direct",
            params={"q": "Springfield", "limit": 3, "appid": API_KEY},
            timeout=10.0
        )

    if response.status_code == 200:
        cities = response.json()
        print(f"✅ SUCCESS!")
        print(f"   Found {len(cities)} cities named 'Springfield':")
        for city in cities:
            state = city.get('state', '')
            state_str = f", {state}" if state else ""
            print(f"   → {city['name']}{state_str}, {city['country']}")
        return True

    print(f"❌ FAIL: Got status code {response.status_code}")
    return False


async def main():
    print("\n🌤️  WEATHER MCP SERVER — TEST SUITE")
    print("=" * 50)

    results = []

    # Run all tests
    results.append(await test_api_key())
    if results[0]:  # Only run API tests if key exists
        results.append(await test_current_weather())
        results.append(await test_forecast())
        results.append(await test_city_search())

    # Summary
    print(f"\n{'='*50}")
    passed = sum(1 for r in results if r)
    total = len(results)

    if passed == total:
        print(f"🎉 ALL {total} TESTS PASSED! Your server is ready.")
    else:
        print(f"⚠️  {passed}/{total} tests passed. Fix the failures above.")

    print("=" * 50)


if __name__ == "__main__":
    asyncio.run(main())
