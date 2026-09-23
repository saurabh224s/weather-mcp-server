# Security

This server uses an external weather API and therefore handles an API credential.

- Store `OPENWEATHER_API_KEY` in `.env` or a secret manager.
- Never commit `.env` or paste a real key into an issue or pull request.
- Rotate a key immediately if it is exposed.
- Only connect the server to MCP clients you trust.

For vulnerabilities, provide affected version/commit, reproducible steps, expected versus observed behavior, and logs with secrets removed.
