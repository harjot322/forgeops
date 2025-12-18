# Simulator App Code

This folder contains the script that generates incident traffic.

## Files

- `simulator.py` – Creates fake incidents and sends them to the API

## How to read it

1) `build_incident()` shows how payloads are generated.
2) `main()` shows how many requests are sent and how fast.

## Key ideas

- Weighted severities create realistic distributions.
- Rate and burst are controlled with environment variables.
