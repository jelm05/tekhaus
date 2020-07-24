# Create your tasks here
from __future__ import absolute_import, unicode_literals

from datetime import timedelta

from celery import shared_task
from celery.task import periodic_task

from checkouts.models import Student, Checkout

# logger = get_task_logger(__name__)


@shared_task
def post_checkout_confirmation_email(user_pk=None, checkout_pk=None):
    user = Student.objects.filter(pk=user_pk)
    checkout = Checkout.objects.filter(pk=checkout_pk)
    if checkout and user:
        print("Checkout Complete! Checkout: {}, User: {}").format(checkout, user)
    else:
        print("No checkout for specified user.")


# @periodic_task(run_every=timedelta(seconds=10))
# def ten_second_task():
#     logger.info("This runs every ten seconds")