# Create your tasks here
from __future__ import absolute_import, unicode_literals

from datetime import timedelta

from celery import shared_task
from celery.task import periodic_task

logger = get_task_logger(__name__)


@shared_task
def add(x, y):
    return x + y


@periodic_task(run_every=timedelta(seconds=10))
def ten_second_task():
    logger.info("This runs every ten seconds")