import time

from app.config import settings
from app.database import SessionLocal
from app.services.email_delivery_service import EmailDeliveryService
from app.services.redis_queue import dequeue_email_job


def run_worker(poll_interval: float = 0.5) -> None:
    last_sweep = 0.0
    while True:
        now = time.time()
        if now - last_sweep >= float(settings.EMAIL_RETRY_SWEEP_INTERVAL_SECONDS):
            db = SessionLocal()
            try:
                EmailDeliveryService.sweep_due_retries(db=db)
            finally:
                db.close()
            last_sweep = now

        item = dequeue_email_job(timeout=1)
        if not item:
            time.sleep(poll_interval)
            continue

        audit_id = item.get('audit_id')
        payload = item.get('payload') or {}
        if not audit_id:
            continue

        db = SessionLocal()
        try:
            EmailDeliveryService.process_audit_send(db=db, audit_id=int(audit_id), payload=payload)
        finally:
            db.close()


if __name__ == '__main__':
    run_worker()
