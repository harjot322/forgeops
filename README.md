# ForgeOps Lab

ForgeOps Lab is a local-first DevOps learning project that shows how incidents move through a system. It simulates a realistic workflow: incidents arrive, get queued, a worker fixes them, and everything is visible in metrics dashboards and logs. It runs entirely on your laptop with Docker Compose and includes an optional AWS free-tier Terraform module (off by default).

If you know the tools but are new to how they fit together, this project is designed as a guided, hands-on tutorial.

## What you will learn

- How a basic incident pipeline works end-to-end
- How queues decouple systems and handle spikes
- How metrics and logs are collected and visualized
- How to connect Prometheus, Grafana, Loki, and Promtail
- How to explore a system from API to database

## Big picture (one-minute mental model)

Think of this project as a tiny “incident factory”:

1) **Simulator** creates fake incidents (like “latency spike”).
2) **API** receives incidents and writes them to **Postgres**.
3) The API also puts a short message into **Redis** (the queue).
4) **Worker** reads the queue, runs a “runbook,” and updates Postgres.
5) **Prometheus** collects metrics from API and worker.
6) **Grafana** shows those metrics as charts.
7) **Promtail + Loki** collect and browse logs.

You can watch the whole pipeline live in minutes.

## Architecture

```
simulator --> api --> redis queue --> worker --> postgres
                 \-> prometheus -> grafana
                 \-> promtail -> loki
```

## Quickstart (local only)

Prereqs: Docker Desktop.

```
cd forgeops-lab
cp .env.example .env
make up
```

Open:
- API docs: http://localhost:8080/docs
- Grafana: http://localhost:3000 (admin / admin)
- Prometheus targets: http://localhost:9090/targets

Generate activity:

```
make simulate
```

## First-time walkthrough (step by step)

### 1) Create a single incident

Open `http://localhost:8080/docs`, expand **POST /incidents**, and submit:

```json
{
  "title": "Latency spike detected",
  "service": "billing",
  "severity": "high"
}
```

You should get back an `incident_id`.

### 2) See it stored

Call **GET /incidents** in the same API docs.
You should see the incident with status `queued` or `resolved`.

### 3) See the system working

Open Grafana and view the **ForgeOps Overview** dashboard.
You should see:
- Intake rate increasing
- Queue depth changing
- Resolution time p95 shifting

### 4) Generate a spike

Run:

```
make simulate
```

This sends many incidents quickly and makes the charts move.

## What each service does (plain English)

- **api**: Front door. Accepts incidents, stores them, and sends a queue message.
- **worker**: Fixer. Pulls incidents from the queue and resolves them.
- **redis**: Queue. Holds incidents while the worker is busy.
- **postgres**: Database. Stores incident history and outcomes.
- **prometheus**: Metrics collector.
- **grafana**: Dashboards and charts.
- **loki + promtail**: Centralized logs.
- **simulator**: Fake traffic generator.

## Deeper dive: what happens when you submit an incident

1) The API writes a new row into the `incidents` table.
2) The API pushes a JSON message into Redis list `incident_queue`.
3) The worker blocks on that queue (BRPOP) and takes the next item.
4) The worker waits a few seconds (simulated runbook), then:
   - Updates the incident status
   - Writes a row into the `incident_runs` table
5) Prometheus scrapes:
   - `api` at `/metrics`
   - `worker` on port `9102`
6) Promtail reads log files and sends them to Loki.
7) Grafana reads from Prometheus + Loki and displays metrics/logs.

## Data model (simple)

`incidents` table:
- id, title, service, severity, status, created_at

`incident_runs` table:
- incident_id, runbook, outcome, resolved_at, resolution_seconds

## Key metrics you can watch

- `incidents_created_total` – how many incidents were received
- `incident_queue_depth` – how many are waiting in Redis
- `incident_resolution_seconds` – how long the worker took
- `incident_processed_total` – resolved vs mitigated counts

## Logs you can explore

Logs are written to a shared volume and scraped by Promtail.
In Grafana, you can explore logs with the **Loki** datasource.

Example log events:
- `incident_created`
- `incident_processed`
- `worker_error`

## Useful commands

```
make up          # start everything
make down        # stop and remove containers
make logs        # tail service logs
make simulate    # run the simulator once
make clean       # remove volumes
```

## Troubleshooting (quick fixes)

- **API not reachable**: wait 10–20 seconds after `make up`.
- **Grafana empty**: generate traffic with `make simulate`.
- **Queue stays high**: worker might be restarting; check `make logs`.
- **Prometheus targets down**: open `http://localhost:9090/targets`.

## Optional AWS free-tier module

Terraform code lives in `infrastructure/aws-free-tier`. It is **not** required for local runs.
It provisions (free-tier safe within normal usage):
- S3 bucket for incident exports
- DynamoDB table for runbook results (on-demand)
- IAM role and policy for optional integrations

Use it only if you want a minimal cloud footprint:

```
cd infrastructure/aws-free-tier
terraform init
terraform apply
```

## Project layout

```
forgeops-lab/
  docker-compose.yml
  Makefile
  services/
  platform/
  docs/
  infrastructure/
```

## Notes

- Everything runs locally; no cloud calls are made by default.
- You can safely delete `infrastructure/aws-free-tier` if you never plan to deploy.
