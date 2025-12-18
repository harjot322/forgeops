# Architecture

ForgeOps Lab models a production-ready incident workflow using local-only services.

## Data flow

1. Simulator posts incidents to the API.
2. API stores incidents in Postgres and enqueues work in Redis.
3. Worker pulls from Redis, executes a runbook, and records outcomes.
4. Prometheus scrapes API/worker metrics.
5. Promtail tails log files and ships to Loki.
6. Grafana visualizes everything.

## Operational behaviors

- **Backpressure aware**: queue depth is tracked and exposed as a metric.
- **Runbook determinism**: severity controls the runbook and resolution profile.
- **Observability by default**: metrics and logs are available without config.

## Failure simulation ideas

- Stop the worker container to observe queue buildup.
- Reduce Redis availability to watch error logs and retries.
- Increase simulator burst for load testing.
