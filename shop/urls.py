from django.urls import path
from . import views

app_name = 'shop'
urlpatterns = [
    path('', views.product_list, name='list'),
    path('<slug:category_slug>/', views.product_list, name='list_item'),
    path('<int:id>/<slug:slug>', views.product_detail, name='detail'),
    
    #For Crud
    path('seller/dashboard/', views.seller_dashboard, name='seller_dashboard'),
    path('seller/product/add/', views.product_create, name='product_create'),
    path('seller/product/edit/<int:pk>/', views.product_update, name='product_update'),
    path('seller/product/delete/<int:pk>/', views.product_delete, name='product_delete'),
    
]
