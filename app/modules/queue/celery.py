from celery import Celery
from ...core.config import config

celery_app = Celery(
    "worker",
    broker=config.CELERY_BROKER,
    backend=config.CELERY_BACKEND
)

# Auto-discover tasks in this module
celery_app.autodiscover_tasks(['app.modules.queue'])

# Import tasks manually to ensure they're registered
from . import task  # noqa: F401