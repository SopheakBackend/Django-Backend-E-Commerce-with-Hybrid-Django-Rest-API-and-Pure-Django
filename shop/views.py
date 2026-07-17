from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category
from cart.forms import CartAddProductForm
from .recommender import Recommend
from django.contrib.auth.decorators import login_required
from .forms import ProductForm
from django.core.exceptions import PermissionDenied

# Create your views here.
def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        language = request.LANGUAGE_CODE
        category = get_object_or_404(
            Category, 
            translations__language_code = language,
            translations__slug = category_slug
        )
        products = Product.objects.filter(category = category)
    return render(request, 'shop/product/list.html', {'category': category, 'categories': categories, 'products': products})
        
def product_detail(request, id, slug):
    language = request.LANGUAGE_CODE

    product = get_object_or_404(
        Product, id = id,
        translations__language_code = language,
        translations__slug = slug,
        available = True
    )
    form = CartAddProductForm()
    
    redis = Recommend()
    recommended_products = redis.suggest_products_for([product], 4)
    return render(request, 'shop/product/detail.html', {'product': product, 'form': form, 'recommended_products': recommended_products})


#For Crud
def user_is_seller(user):
    return user.is_authenticated and hasattr(user, 'seller_profile') and user.seller_profile.is_seller
@login_required
def seller_dashboard(request):
    if not user_is_seller(request.user):
        return redirect('products:product_list') 
    my_products = Product.objects.filter(seller=request.user)
    
    return render(request, 'shop/seller/dashboard.html', {'products': my_products})
@login_required
def product_create(request):
    if not user_is_seller(request.user):
        return redirect('products:product_list')

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES) 
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()
            return redirect('shop:seller_dashboard')
    else:
        form = ProductForm()
        
    return render(request, 'shop/seller/product_form.html', {'form': form, 'action': 'Create'})
@login_required
def product_update(request, pk):
    if not user_is_seller(request.user):
        return redirect('products:product_list')
    product = get_object_or_404(Product, pk=pk, seller=request.user)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('shop:seller_dashboard')
    else:
        form = ProductForm(instance=product)
        
    return render(request, 'shop/seller/product_form.html', {'form': form, 'action': 'Update', 'product': product})
@login_required
def product_delete(request, pk):
    if not user_is_seller(request.user):
        return redirect('products:product_list')

    product = get_object_or_404(Product, pk=pk, seller=request.user)

    if request.method == 'POST':
        product.delete()
        return redirect('shop:seller_dashboard')
        
    return render(request, 'shop/seller/product_confirm_delete.html', {'product': product})
