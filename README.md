# 🌤️ Weather MCP Server

An MCP (Model Context Protocol) server that provides weather tools backed by the OpenWeatherMap API.

## Features

| Tool | Description |
| --- | --- |
| `get_current_weather` | Get current conditions for a city. |
| `get_weather_forecast` | Get a forecast for up to five days. |
| `search_cities` | Find cities by name and disambiguate locations. |

## Requirements

- Python 3.11+
- An OpenWeatherMap API key
- An MCP-compatible client such as Claude Desktop

## Quick start

1. Create a virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

   On Windows PowerShell, use `.venv\\Scripts\\Activate.ps1`.

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Create your environment file:

   ```bash
   cp .env.example .env
   ```

4. Set `OPENWEATHER_API_KEY` in `.env`.

5. Run the smoke-test script:

   ```bash
   python test_server.py
   ```

6. Start the MCP server:

   ```bash
   python src/weather_server.py
   ```

## GitHub Codespaces

The repository includes a Dev Container configuration. Open the repository in Codespaces and dependencies are installed automatically.

Do not commit your real API key. Keep credentials in `.env`, and make sure local secret files remain ignored by Git.

## Claude Desktop

Configure Claude Desktop to launch `src/weather_server.py` with the `OPENWEATHER_API_KEY` environment variable. The exact configuration path depends on your operating system and Claude Desktop installation.

## Contributing

Small, focused improvements are welcome. Before opening a pull request:

1. Read the existing project structure and contribution requirements.
2. Keep changes focused and explain the user-facing benefit.
3. Run the available tests or smoke checks.
4. Never include API keys, tokens, or other secrets in commits.

For larger changes, open an issue first so the proposed approach can be discussed.

## License

See the repository's license file for licensing terms.
