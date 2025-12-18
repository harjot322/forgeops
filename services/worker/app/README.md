# Worker App Code

This folder contains the worker process that consumes queue items and resolves incidents.

## Files

- `worker.py` – Main worker loop and runbook simulation

## How to read it

1) Find `main()` to see the worker loop.
2) Check `simulate_runbook()` to understand timing and outcomes.
3) Look at `update_incident()` to see how results are stored.

## Key ideas

- The worker blocks on Redis to wait for work.
- Resolution time is simulated to create realistic metrics.
- Outcomes are written to Postgres for history and dashboards.
