# Create your tasks here
from __future__ import absolute_import, unicode_literals
from django.shortcuts import get_object_or_404

from celery import shared_task
from celery.utils.log import get_task_logger


from checkouts.models import Checkout
from checkouts.utils import email_pdf

logger = get_task_logger(__name__)


@shared_task
def hello():
    print("Hello World!")


@shared_task
def post_checkout_confirmation_email(checkout_pk=None):
    checkout = get_object_or_404(Checkout, pk=checkout_pk)

    subject = 'Checkout #{}'.format(checkout.id)
    body = 'This confirms your equipment checkout. Please attached PDF for details.'
    from_address = 'vcs@sva.edu'
    to_address = checkout.student.primary_email
    # bcc_address = checkout.processed_by.email

    cameras = checkout.cameras.all()
    lights = checkout.lights.all()
    computers = checkout.computers.all()
    projectors = checkout.projectors.all()
    audio = checkout.audio.all()
    misc = checkout.misc.all()
    equipment = cameras | lights | computers | projectors | audio | misc

    data = {
        'checkout_number': checkout,
        'first_name': checkout.student.first_name,
        'last_name': checkout.student.last_name,
        'user_id': checkout.student.school_id,
        'date_issued': checkout.borrow_date,
        'due_date': checkout.due_date,
        'staff_first': checkout.processed_by.first_name,
        'staff_last': checkout.processed_by.last_name,
        'notes': checkout.notes,
        'equipment': equipment,
    }
    email_pdf('pdf/completed-checkout-pdf.html', data, subject, body, from_address, to_address)
