# Worker Service

The worker is the “fixer” in the system. It consumes incidents from Redis, simulates a runbook, and writes the outcome back to Postgres. It also exposes Prometheus metrics so you can watch performance.

## What it does (plain English)

- Waits on the Redis queue
- Takes the next incident message
- Runs a simulated “runbook” based on severity
- Writes the result to Postgres
- Emits metrics and logs

## Key files

- `app/worker.py` – The worker process
- `requirements.txt` – Python dependencies
- `Dockerfile` – Container build recipe

## Walking through `app/worker.py`

### 1) Queue consumption

The worker uses `BRPOP` to wait for items in `incident_queue`. This blocks until there is work, which is efficient and realistic.

### 2) Runbook simulation

A runbook is selected based on severity:

- low -> `cache_flush`
- medium -> `deploy_rollback`
- high -> `traffic_shift`
- critical -> `global_failover`

Each severity has a simulated duration range. This creates realistic-looking charts.

### 3) Database updates

Once a runbook “finishes”:

- The incident status is updated (e.g., `resolved` or `mitigated`).
- A row is written to `incident_runs` with timing information.

### 4) Metrics you can see

- `incident_processed_total{outcome=...}`
- `incident_resolution_seconds`
- `incident_in_progress`

## Try it manually

1) Create an incident in the API docs.
2) Watch logs in the worker:

```
make logs
```

You should see `incident_processed` events.

## Why this design

This models real production patterns:
- Queues smooth traffic spikes.
- Work is separated from the API for reliability.
- Metrics tell you if the system is healthy.
