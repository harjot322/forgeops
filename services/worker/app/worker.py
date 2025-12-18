import json
import logging
import os
import random
import time
from datetime import datetime, timezone

import psycopg2
import redis
from prometheus_client import Counter, Histogram, Gauge, start_http_server

LOG_DIR = os.getenv("LOG_DIR", "/var/log/forgeops")
LOG_PATH = os.path.join(LOG_DIR, "worker.log")

os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[logging.FileHandler(LOG_PATH), logging.StreamHandler()],
)

logger = logging.getLogger("forgeops.worker")

INCIDENTS_PROCESSED = Counter(
    "incident_processed_total",
    "Total incidents processed",
    ["outcome"],
)
INCIDENT_RESOLUTION = Histogram(
    "incident_resolution_seconds",
    "Incident resolution time",
)
INCIDENTS_IN_PROGRESS = Gauge(
    "incident_in_progress",
    "Incidents being processed",
)

RUNBOOKS = {
    "low": "cache_flush",
    "medium": "deploy_rollback",
    "high": "traffic_shift",
    "critical": "global_failover",
}


def connect_postgres():
    return psycopg2.connect(
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT"),
        dbname=os.getenv("POSTGRES_DB"),
    )


def connect_redis():
    return redis.Redis(
        host=os.getenv("REDIS_HOST"),
        port=int(os.getenv("REDIS_PORT", "6379")),
        decode_responses=True,
    )


def simulate_runbook(severity):
    base = {
        "low": (1, 2),
        "medium": (2, 4),
        "high": (4, 6),
        "critical": (6, 8),
    }[severity]
    duration = random.uniform(*base)
    time.sleep(duration)
    outcome = "resolved" if random.random() > 0.05 else "mitigated"
    return duration, outcome


def update_incident(conn, incident_id, outcome, runbook, duration):
    with conn.cursor() as cur:
        cur.execute(
            "UPDATE incidents SET status = %s WHERE id = %s;",
            (outcome, incident_id),
        )
        cur.execute(
            """
            INSERT INTO incident_runs (incident_id, runbook, outcome, resolved_at, resolution_seconds)
            VALUES (%s, %s, %s, %s, %s);
            """,
            (
                incident_id,
                runbook,
                outcome,
                datetime.now(timezone.utc),
                int(duration),
            ),
        )
    conn.commit()


def main():
    metrics_port = int(os.getenv("WORKER_METRICS_PORT", "9102"))
    start_http_server(metrics_port)
    redis_client = connect_redis()

    while True:
        try:
            payload = redis_client.brpop("incident_queue", timeout=5)
            if not payload:
                continue
            _, data = payload
            incident = json.loads(data)
            INCIDENTS_IN_PROGRESS.inc()
            start_time = time.time()

            duration, outcome = simulate_runbook(incident["severity"])
            conn = connect_postgres()
            update_incident(
                conn,
                incident["incident_id"],
                outcome,
                RUNBOOKS[incident["severity"]],
                duration,
            )
            conn.close()

            INCIDENTS_IN_PROGRESS.dec()
            INCIDENTS_PROCESSED.labels(outcome).inc()
            INCIDENT_RESOLUTION.observe(time.time() - start_time)

            logger.info(
                json.dumps(
                    {
                        "event": "incident_processed",
                        "incident_id": incident["incident_id"],
                        "severity": incident["severity"],
                        "outcome": outcome,
                        "runbook": RUNBOOKS[incident["severity"]],
                    }
                )
            )
        except Exception as exc:
            logger.info(json.dumps({"event": "worker_error", "error": str(exc)}))
            time.sleep(2)


if __name__ == "__main__":
    main()
