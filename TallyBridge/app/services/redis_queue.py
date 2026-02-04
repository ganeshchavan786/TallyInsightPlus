"""Redis Queue Helpers

Minimal Redis helpers for enqueue/dequeue of export jobs.

This is intentionally small and dependency-light so we can later swap to a
full job framework (ARQ/RQ/Celery) without rewriting API endpoints.
"""

import json
from typing import Any, Dict, Optional

import redis

from app.config import settings


def get_redis_client() -> redis.Redis:
    return redis.Redis.from_url(settings.REDIS_URL, decode_responses=True)


def enqueue_export_job(job_id: int, payload: Optional[Dict[str, Any]] = None) -> None:
    client = get_redis_client()
    message = {
        "job_id": job_id,
        "payload": payload or {},
    }
    client.rpush(settings.EXPORT_JOBS_QUEUE_NAME, json.dumps(message))


def dequeue_export_job(timeout: int = 5) -> Optional[Dict[str, Any]]:
    client = get_redis_client()
    item = client.brpop(settings.EXPORT_JOBS_QUEUE_NAME, timeout=timeout)
    if not item:
        return None
    _, raw = item
    try:
        return json.loads(raw)
    except Exception:
        return {"job_id": None, "payload": {}, "raw": raw}


def enqueue_email_job(audit_id: int, payload: Dict[str, Any]) -> None:
    client = get_redis_client()
    item = {
        "audit_id": audit_id,
        "payload": payload,
    }
    client.lpush(settings.EMAIL_JOBS_QUEUE_NAME, json.dumps(item))


def dequeue_email_job(timeout: int = 5) -> Optional[Dict[str, Any]]:
    client = get_redis_client()
    item = client.brpop(settings.EMAIL_JOBS_QUEUE_NAME, timeout=timeout)
    if not item:
        return None
    _, raw = item
    try:
        return json.loads(raw)
    except Exception:
        return {"audit_id": None, "payload": {}, "raw": raw}
