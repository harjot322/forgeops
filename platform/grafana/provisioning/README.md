# Grafana Provisioning

Grafana can auto-load datasources and dashboards on startup. This folder contains those provisioning files.

## Structure

- `datasources/` – Defines Prometheus and Loki connections
- `dashboards/` – Tells Grafana where to load dashboards from

## Why it matters

Provisioning removes manual setup. You can recreate the entire stack and dashboards will appear automatically.
