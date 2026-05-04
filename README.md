# 🌤️ Weather MCP Server

An MCP (Model Context Protocol) server that wraps the OpenWeatherMap API.
Connect it to Claude Desktop to give Claude real-time weather superpowers!

## 🛠️ Tools Available

| Tool | What it does |
|------|-------------|
| `get_current_weather` | Current temperature, humidity, wind, etc. for any city |
| `get_weather_forecast` | Up to 5-day forecast for any city |
| `search_cities` | Find cities by name (helps with ambiguous names) |

## 🚀 Running on GitHub Codespaces (Recommended)

1. Click the green **Code** button above
2. Click **Codespaces** tab
3. Click **Create codespace on main**
4. Wait for it to load (~2 minutes)
5. In the terminal that opens, create your `.env` file:
   ```bash
   cp .env.example .env
