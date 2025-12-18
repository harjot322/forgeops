import os
import random
import time

import httpx

API_URL = os.getenv("API_URL", "http://localhost:8080")
SIMULATOR_RATE = int(os.getenv("SIMULATOR_RATE", "20"))
SIMULATOR_BURST = int(os.getenv("SIMULATOR_BURST", "40"))

SERVICES = ["billing", "edge", "search", "auth", "catalog", "pipeline"]
SEVERITIES = ["low", "medium", "high", "critical"]
TITLES = [
    "Latency spike detected",
    "Pod crash loop",
    "Queue backlog rising",
    "Disk saturation risk",
    "TLS handshake failures",
    "Cache stampede",
]


def build_incident():
    return {
        "title": random.choice(TITLES),
        "service": random.choice(SERVICES),
        "severity": random.choices(SEVERITIES, weights=[50, 30, 15, 5])[0],
    }


def main():
    with httpx.Client(timeout=5.0) as client:
        for _ in range(SIMULATOR_BURST):
            payload = build_incident()
            response = client.post(f"{API_URL}/incidents", json=payload)
            if response.status_code >= 400:
                print("Failed to send incident", response.text)
            time.sleep(1 / SIMULATOR_RATE)


if __name__ == "__main__":
    main()
