import json
import logging
import os
import time
from datetime import datetime, timezone

import psycopg2
import redis
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from prometheus_client import Counter, Histogram, Gauge, make_asgi_app

LOG_DIR = os.getenv("LOG_DIR", "/var/log/forgeops")
LOG_PATH = os.path.join(LOG_DIR, "api.log")

os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[logging.FileHandler(LOG_PATH), logging.StreamHandler()],
)

logger = logging.getLogger("forgeops.api")

DB_RETRY_SECONDS = 30

INCIDENTS_CREATED = Counter(
    "incidents_created_total",
    "Total incidents created",
    ["severity"],
)
INCIDENT_CREATE_LATENCY = Histogram(
    "incident_create_duration_seconds",
    "Incident creation latency",
)
INCIDENT_QUEUE_DEPTH = Gauge(
    "incident_queue_depth",
    "Queue depth for incidents",
)

app = FastAPI(title="ForgeOps API", version="1.0")
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)


class IncidentIn(BaseModel):
    title: str = Field(..., min_length=5, max_length=120)
    service: str = Field(..., min_length=2, max_length=40)
    severity: str = Field(..., pattern=r"^(low|medium|high|critical)$")


def connect_postgres():
    deadline = time.time() + DB_RETRY_SECONDS
    while True:
        try:
            return psycopg2.connect(
                user=os.getenv("POSTGRES_USER"),
                password=os.getenv("POSTGRES_PASSWORD"),
                host=os.getenv("POSTGRES_HOST"),
                port=os.getenv("POSTGRES_PORT"),
                dbname=os.getenv("POSTGRES_DB"),
            )
        except psycopg2.OperationalError as exc:
            if time.time() > deadline:
                raise exc
            logger.info(json.dumps({"event": "postgres_retry", "error": str(exc)}))
            time.sleep(2)


def ensure_tables(conn):
    with conn.cursor() as cur:
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS incidents (
                id SERIAL PRIMARY KEY,
                title TEXT NOT NULL,
                service TEXT NOT NULL,
                severity TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'queued',
                created_at TIMESTAMP NOT NULL
            );
            """
        )
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS incident_runs (
                id SERIAL PRIMARY KEY,
                incident_id INTEGER NOT NULL REFERENCES incidents(id),
                runbook TEXT NOT NULL,
                outcome TEXT NOT NULL,
                resolved_at TIMESTAMP NOT NULL,
                resolution_seconds INTEGER NOT NULL
            );
            """
        )
    conn.commit()


@app.on_event("startup")
def startup():
    conn = connect_postgres()
    ensure_tables(conn)
    conn.close()


@app.get("/health")
def health():
    return {"status": "ok", "time": datetime.now(timezone.utc).isoformat()}


@app.post("/incidents")
def create_incident(payload: IncidentIn):
    start_time = time.time()
    conn = connect_postgres()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO incidents (title, service, severity, status, created_at)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id;
                """,
                (
                    payload.title,
                    payload.service,
                    payload.severity,
                    "queued",
                    datetime.now(timezone.utc),
                ),
            )
            incident_id = cur.fetchone()[0]
        conn.commit()
    finally:
        conn.close()

    queue_payload = {
        "incident_id": incident_id,
        "severity": payload.severity,
        "service": payload.service,
        "title": payload.title,
    }
    redis_client = redis.Redis(
        host=os.getenv("REDIS_HOST"),
        port=int(os.getenv("REDIS_PORT", "6379")),
        decode_responses=True,
    )
    redis_client.lpush("incident_queue", json.dumps(queue_payload))
    INCIDENT_QUEUE_DEPTH.set(redis_client.llen("incident_queue"))

    INCIDENTS_CREATED.labels(payload.severity).inc()
    INCIDENT_CREATE_LATENCY.observe(time.time() - start_time)

    logger.info(
        json.dumps(
            {
                "event": "incident_created",
                "incident_id": incident_id,
                "severity": payload.severity,
                "service": payload.service,
            }
        )
    )
    return {"incident_id": incident_id, "status": "queued"}


@app.get("/incidents")
def list_incidents(limit: int = 20):
    if limit > 100:
        raise HTTPException(status_code=400, detail="limit too high")
    conn = connect_postgres()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, title, service, severity, status, created_at
                FROM incidents
                ORDER BY created_at DESC
                LIMIT %s;
                """,
                (limit,),
            )
            rows = cur.fetchall()
    finally:
        conn.close()

    return [
        {
            "id": row[0],
            "title": row[1],
            "service": row[2],
            "severity": row[3],
            "status": row[4],
            "created_at": row[5].isoformat(),
        }
        for row in rows
    ]
