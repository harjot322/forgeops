# API App Code

This folder contains the actual FastAPI application code. The rest of the `api/` folder is packaging and dependencies.

## Files

- `main.py` – Defines routes, database setup, queueing, and metrics

## How to read it (suggested order)

1) **Startup**: find the `startup()` function to see table creation.
2) **Models**: `IncidentIn` shows the input shape.
3) **POST /incidents**: the core incident intake flow.
4) **GET /incidents**: list endpoint used for verification.

## Key ideas

- API writes to Postgres first, then queues work in Redis.
- Metrics are exported using Prometheus client.
- Logs are JSON so they are easy to query in Loki.
