# Grafana Datasources

This folder defines data sources Grafana connects to automatically.

## Files

- `datasources.yml` – Adds Prometheus (metrics) and Loki (logs)

## How it works

When Grafana starts, it reads this file and connects to the configured URLs. This avoids clicking through the UI each time you restart.
