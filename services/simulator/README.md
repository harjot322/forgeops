# Simulator Service

The simulator generates fake incidents so you can see the system working without manual input. It sends HTTP requests to the API in bursts.

## What it does

- Builds realistic incident payloads
- Sends them to the API at a controlled rate
- Creates enough activity to populate dashboards

## Key files

- `app/simulator.py` – The traffic generator
- `requirements.txt` – Python dependencies
- `Dockerfile` – Container build recipe

## How it works

- `SIMULATOR_BURST` = number of incidents to send
- `SIMULATOR_RATE` = incidents per second
- `API_URL` = API endpoint to target

It randomly picks:
- service name (billing, auth, search, etc.)
- severity (weighted toward low/medium)
- incident title

## Run it

From the project root:

```
make simulate
```

## Why this is useful

Most demos fail because nothing is happening. This service ensures you can always generate traffic and instantly see metrics and logs change.
