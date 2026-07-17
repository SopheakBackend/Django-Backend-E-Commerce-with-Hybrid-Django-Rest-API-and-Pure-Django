# api/urls.py
from django.urls import path
from .views import api_register_view, api_login_view
from .views import login_page, register_page, logout_page

urlpatterns = [
    path('login/', login_page, name='html_login'),
    path('register/', register_page, name='html_register'),
    path('logout/', logout_page, name='html_logout'),

    #API
    path('auth/login/', api_login_view, name='api_login'),
    path('auth/register/', api_register_view, name='api_register'),
]
