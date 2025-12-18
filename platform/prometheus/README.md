# Prometheus

Prometheus is the metrics collector. It scrapes the API and worker on a schedule and stores time-series data locally.

## Files

- `prometheus.yml` – Scrape configuration

## What it scrapes

- `api:8080/metrics` – incident intake and queue metrics
- `worker:9102` – processing metrics
- `prometheus:9090` – Prometheus itself

## How to check

Open `http://localhost:9090/targets` and ensure all targets are UP.

## Why it matters

Metrics show system health trends. In this project, they show:
- How many incidents are coming in
- How deep the queue is
- How long resolutions take
