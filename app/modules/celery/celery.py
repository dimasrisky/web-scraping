from celery import Celery

celery_app = Celery(
    "worker_scraping",
    broker=""
)