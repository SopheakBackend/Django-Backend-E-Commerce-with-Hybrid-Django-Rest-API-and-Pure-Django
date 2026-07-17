import stripe 
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from orders.models import Order
from payment.task import payment_completed
from shop.models import Product
from shop.recommender import Recommend
@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.headers.get('stripe-signature')
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)
    
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object'] 
        if session['mode'] == 'payment' and session['payment_status'] == 'paid':
            try:
                order = Order.objects.get(
                id=session.get('client_reference_id')
                )
            except Order.DoesNotExist:
                return HttpResponse(status=404)
                # mark order as paid
            order.paid = True
            order.stripe_id = session.get('payment_intent')
            order.save()
            
            #save items bought for product recommendations
            products_ids = order.items.values_list('product_id')
            products = Product.objects.filter(id__in = products_ids )
            redis = Recommend()
            redis.product_bought(products)
            payment_completed.delay(order.id)
            

    return HttpResponse(status=200)
                
    
        
     
    
