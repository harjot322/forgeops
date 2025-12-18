# Services

This folder contains the application services that simulate a full incident workflow. Each service is containerized and wired together in `docker-compose.yml`.

## Services overview

- `api/` – Accepts incidents, stores them, enqueues work, exposes metrics.
- `worker/` – Pulls incidents from Redis, runs a runbook, writes outcomes.
- `simulator/` – Generates realistic incident traffic for demos and testing.

## How the services interact

1) The simulator calls the API with fake incidents.
2) The API writes the incident to Postgres and pushes a message into Redis.
3) The worker reads from Redis and updates Postgres.
4) Both API and worker expose Prometheus metrics.

## Learning tips

- Start by reading `api/app/main.py` to understand the entry point.
- Then read `worker/app/worker.py` to see how the queue is processed.
- Use the simulator last to generate load and watch the metrics change.

## Run locally

From the project root:

```
make up
make simulate
```

## Where to go next

Each service folder contains its own README with a guided, tutorial-style explanation:
- `services/api/README.md`
- `services/worker/README.md`
- `services/simulator/README.md`
