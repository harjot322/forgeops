# Promtail

Promtail is the log shipper. It reads log files on disk and sends them to Loki.

## Files

- `promtail.yml` – Promtail configuration

## What it does here

- Reads JSON logs from `/var/log/forgeops/*.log`
- Labels them with `job=forgeops`
- Sends them to `http://loki:3100`

## How to verify

1) Open Grafana
2) Go to **Explore**
3) Select **Loki** datasource
4) Query: `{job="forgeops"}`

If you have run `make simulate`, you should see logs from API and worker.
