from io import BytesIO

import weasyprint
from celery import shared_task
from django.contrib.staticfiles import finders
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from orders.models import Order
from django.conf import settings

@shared_task
def payment_completed(order_id):
    order = Order.objects.get(id=order_id)
    subject = f'My Shop - Invoice no. {order.id}'
    message = (
        'Please, find attached the invoice for your recent purchase.'
    )
    email = EmailMessage(
        subject, message, from_email=settings.DEFAULT_FROM_EMAIL , to=[order.email]
    )
    html = render_to_string('orders/order/pdf.html', {'order': order})
    out = BytesIO()
    weasyprint.HTML(string=html).write_pdf(
        out, 
        stylesheets= [weasyprint.CSS(finders.find('css/pdf.css'))]
    )
    email.attach(
        f'order_{order.id}.pdf', out.getvalue(), 'application/pdf'
    )
    
    email.send()