# Loki

Loki is the log database. It stores logs sent by Promtail and makes them searchable in Grafana.

## Files

- `loki.yml` – Loki configuration

## How it works here

- Loki runs in a single-container mode (no clustering).
- Logs are stored locally inside the container filesystem.
- Promtail sends logs from `/var/log/forgeops`.

## Why it matters

Metrics tell you *what* is happening; logs show *why*. Loki lets you explore the JSON log events produced by the API and worker.
