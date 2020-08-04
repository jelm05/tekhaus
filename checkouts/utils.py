from io import BytesIO

from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.template.loader import get_template

from xhtml2pdf import pisa


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument( BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        print(type(pdf))
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


def email_pdf(template_src, context_dict, subject, body, from_address, to_address):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument( BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        response = HttpResponse(result.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = 'filename="checkout_confirmation.pdf"'
        email = EmailMessage(subject, body, from_address, [to_address])
        # email = EmailMessage(subject, body, from_address, [to_address, bcc_address])
        email.attach('checkout_confirmation.pdf', result.getvalue(), 'application/pdf')
        email.send()
        print("email sent")
    return None

