from django import template
register = template.Library()


@register.simple_tag
def return_date_calc(return_date, due_date):
    diff = return_date - due_date
    # ABS makes negative number positive
    return abs(diff.days)