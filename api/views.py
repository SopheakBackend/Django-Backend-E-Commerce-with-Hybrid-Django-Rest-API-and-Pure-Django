from django.shortcuts import render, redirect
from django.contrib.auth import logout 
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from shop.models import SellerProfile 
@api_view(['POST'])
@permission_classes([AllowAny])
def api_register_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')
    wants_to_be_seller = request.data.get('is_seller', False)

    if not username or not password:
        return Response({"error": "Username and password are required."}, status=status.HTTP_400_BAD_REQUEST)
    if User.objects.filter(username=username).exists():
        return Response({"error": "Username is already taken."}, status=status.HTTP_400_BAD_REQUEST)

    print("=== REGISTER DEBUG ===")
    print("Raw is_seller from request:", wants_to_be_seller)
    print("Type:", type(wants_to_be_seller))
    user = User.objects.create_user(username=username, email=email, password=password)

    profile, created = SellerProfile.objects.get_or_create(user=user)
    profile.is_seller = wants_to_be_seller
    profile.save()
    login(request, user) 
    print("Saved profile.is_seller =", profile.is_seller)
    refresh = RefreshToken.for_user(user)

    return Response({
        "is_seller": wants_to_be_seller,
        "tokens": {"refresh": str(refresh), "access": str(refresh.access_token)}
    }, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([AllowAny])
def api_login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user) 
        refresh = RefreshToken.for_user(user)
        
        is_seller = getattr(user.seller_profile, 'is_seller', False)
        return Response({
            "is_seller": is_seller,
            "tokens": {"refresh": str(refresh), "access": str(refresh.access_token)}
        }, status=status.HTTP_200_OK)
    
    return Response({"error": "Invalid username or password."}, status=status.HTTP_400_BAD_REQUEST)

def login_page(request):
    if request.user.is_authenticated:
        return redirect('shop:list') 
    return render(request, 'api/login.html')

def register_page(request):
    if request.user.is_authenticated:
        return redirect('/')
    return render(request, 'api/register.html')

def logout_page(request):
    logout(request)
    return render(request, 'api/logout.html')