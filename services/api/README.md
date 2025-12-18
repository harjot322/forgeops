# API Service (FastAPI)

The API is the entry point to the system. It accepts incidents, stores them in Postgres, and enqueues work in Redis for the worker to process. It also exposes Prometheus metrics.

## What it does (plain English)

- Receives incidents from users or the simulator
- Writes incidents into the database
- Pushes a queue message to Redis
- Exposes `/metrics` for Prometheus
- Logs structured events to a file

## Key files

- `app/main.py` – Main FastAPI application
- `requirements.txt` – Python dependencies
- `Dockerfile` – Container build recipe

## Walking through `app/main.py`

### 1) Configuration and logging

- The service reads environment variables for Postgres and Redis.
- Logs are written to `/var/log/forgeops/api.log` so Promtail can collect them.

### 2) Database setup

On startup, the API connects to Postgres and ensures two tables exist:

- `incidents` – the incident record
- `incident_runs` – the resolution history from the worker

This allows the system to start from scratch without a manual SQL setup.

### 3) API endpoints

- `GET /health` – Quick health check
- `POST /incidents` – Create a new incident (main entry)
- `GET /incidents` – List recent incidents
- `GET /metrics` – Prometheus metrics endpoint

### 4) The incident creation flow

When you call `POST /incidents`:

1) The API inserts a row into the `incidents` table.
2) It creates a JSON message with the incident ID and details.
3) It pushes the message into the Redis list `incident_queue`.
4) It records metrics like intake rate and queue depth.

### 5) Metrics you can see

- `incidents_created_total{severity=...}`
- `incident_create_duration_seconds`
- `incident_queue_depth`

## Try it manually

Open the docs: `http://localhost:8080/docs`

Example payload:

```json
{
  "title": "TLS handshake failures",
  "service": "edge",
  "severity": "medium"
}
```

Then call `GET /incidents` to see it stored.

## Why this design

This pattern is common in production systems:
- The API remains fast by offloading work to a queue.
- The worker can scale separately.
- Observability is baked in from the start.
