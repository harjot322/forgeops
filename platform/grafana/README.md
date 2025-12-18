# Grafana

Grafana is the visualization layer. It reads metrics from Prometheus and logs from Loki and displays them in dashboards.

## Files

- `provisioning/datasources/datasources.yml` – Sets Prometheus and Loki as datasources
- `provisioning/dashboards/dashboards.yml` – Loads dashboards automatically
- `dashboards/forgeops-overview.json` – Main dashboard for the project

## How to use it

1) Open `http://localhost:3000`
2) Login with `admin / admin`
3) Open the **ForgeOps Overview** dashboard

## What the dashboard shows

- Intake rate (incidents per minute)
- Resolution time (p95)
- Queue depth
- Processed outcomes

## Explore logs

Go to **Explore**, select the **Loki** datasource, and filter by `job="forgeops"`.
