from datetime import datetime
from django import template

register = template.Library()


@register.filter
def overdue(due_date):
    # due_date is <class 'datetime.date'>
    # today is <class 'datetime.datetime'>
    # so have to today.date() to convert to datetime.date for comparison
    now = datetime.today()
    today = now.date()

    # OVERDUE:
    if today > due_date:
        return True

    # NOT OVERDUE:
    elif due_date >= today:
        return False


@register.filter
def overdue_days(due_date):
    now = datetime.today()
    today = now.date()

    # OVERDUE:
    if today > due_date:
        diff = today - due_date
        return diff.days

    # NOT OVERDUE:
    elif due_date >= today:
        diff = due_date - today
        return diff.days


# @register.filter('return_date_calculator')
# def return_date_calc(return_date, due_date):
#     days = return_date - due_date
#     return days
