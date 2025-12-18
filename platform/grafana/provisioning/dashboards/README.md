# Grafana Dashboard Provisioning

This folder tells Grafana where dashboards live on disk.

## Files

- `dashboards.yml` – Points Grafana to `/var/lib/grafana/dashboards`

## How it works

Grafana reads this file at startup and automatically loads any dashboards found in the configured path.
