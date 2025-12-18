# Platform (Observability Stack)

This folder configures the observability platform used by ForgeOps Lab. These services collect metrics and logs, then visualize them in dashboards.

## Components

- `prometheus/` – Scrapes metrics from API and worker.
- `grafana/` – Dashboards for metrics and log exploration.
- `loki/` – Log database for structured logs.
- `promtail/` – Log shipper that tails local log files.

## How it works (simple flow)

1) API and worker expose Prometheus metrics.
2) Prometheus scrapes those endpoints on a schedule.
3) API and worker write JSON logs to `/var/log/forgeops`.
4) Promtail reads those log files and sends them to Loki.
5) Grafana visualizes both Prometheus metrics and Loki logs.

## What to explore

- Prometheus targets: `http://localhost:9090/targets`
- Grafana dashboards: `http://localhost:3000`
- Grafana Explore (Logs): select the Loki datasource

## Folder guide

Each subfolder includes its own README with deeper explanations and file-by-file notes:
- `platform/prometheus/README.md`
- `platform/grafana/README.md`
- `platform/loki/README.md`
- `platform/promtail/README.md`
