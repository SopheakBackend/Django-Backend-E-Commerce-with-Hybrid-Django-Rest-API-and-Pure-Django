from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from .cart import Cart
from .forms import CartAddProductForm
from shop.models import Product
from coupons.forms import CouponApplyForm
from shop.recommender import Recommend

# Create your views here.
@require_POST
def cart_add(request, id):
    cart = Cart(request)
    product = get_object_or_404(
        Product, id=id
    )
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product = product, quantity=cd['quantity'],  override_quantity=cd['override'])
    return redirect('cart:detail')
@require_POST
def cart_remove(request, id):
    cart = Cart(request)
    product = get_object_or_404(
        Product, id=id
    )
    cart.remove(product)
    return redirect('cart:detail')
def cart_detail(request):
    cart = Cart(request)
    
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'], 'override': True})
    r = Recommend()
    cart_products = [item['product'] for item in cart]
    if cart_products:
        recommended_products = r.suggest_products_for(cart_products, max_results=4)
    else:
        recommended_products = None
    form = CouponApplyForm()
    
    return render(request, 'cart/detail.html', {'cart': cart, 'form': form, 'recommended_products': recommended_products})

#This is the same detail cart, but with better stabiliy and
# does not trigger the __iter__ and get a new fresh copy of the cart,
#which might messed up the looping inside cart_detail

# def cart_detail(request):
#     cart = Cart(request)
#     cart_items = []
    
#     for item in cart:
#         item['update_quantity_form'] = CartAddProductForm(
#             initial={
#                 'quantity': item['quantity'],
#                 'override': True
#             }
#         )
#         cart_items.append(item)   # Save the enriched items
    
    # return render(request, 'cart/detail.html', {
    #     'cart': cart, 
    #     'cart_items': cart_items   # Pass enriched list instead
    # })