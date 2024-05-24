import os
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
import requests
from .models import UserStock
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
import json
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from rest_framework.views import APIView
from rest_framework import permissions
import json
from types import SimpleNamespace
from dotenv import load_dotenv

load_dotenv()


# Create your views here.
# users/views.py



@csrf_exempt
def register(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        confirm_password = data.get('confirmPassword')
        print(password, " vanvnal ", confirm_password)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'status': 'error', 'message': 'Username already exists'}, status=400)
        if password != confirm_password:
            return JsonResponse({'status': 'error', 'message': 'Passwords do not match'}, status=400)

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        return JsonResponse({'status': 'created', 'message': 'User created successfully'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        print(data)
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            print("authenticated = " ,user.is_authenticated)
            return JsonResponse({'status': 'success', 'message': 'Logged in successfully'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid credentials'}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)

API_KEY = os.environ.get('ALPHA_VANTAGE_KEY')
INTERVAL = '5min'


@method_decorator(csrf_protect, name='dispatch')
class user_stocks_view(APIView):
    permission_classes = (permissions.AllowAny, IsAuthenticated)

    def get(self, request, format=None):
        # Fetch all stocks for the logged-in user
        user_stocks = UserStock.objects.filter(user=request.user)
        res_stocks = []
        for stock in user_stocks:
            url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={stock.stock}&interval={INTERVAL}&apikey={API_KEY}'
            response = requests.get(url)
            data = response.json()
            
            if 'Time Series (5min)' not in data:
                return Response({'error': 'Invalid symbol or API request failed'}, status=status.HTTP_400_BAD_REQUEST)

            latest_data = list(data['Time Series (5min)'].values())[0]
            latest = {
                'symbol': stock.stock,
                'open': latest_data['1. open'],
                'high': latest_data['2. high'],
                'low': latest_data['3. low'],
                'close': latest_data['4. close'],
                'volume': latest_data['5. volume']
            }
            res_stocks.append(latest)

        return Response(res_stocks)

    def post(self, request, format=None):
        # Add a stock to the user's watchlist
        
        symbol = request.data.get('symbol')
        print(symbol)
        if not symbol:
            return JsonResponse({'status': 'error', 'message': 'symbol is required'}, status=400)

        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval={INTERVAL}&apikey={API_KEY}'
        response = requests.get(url)
        data = response.json()

        if 'Time Series (5min)' not in data:
                return JsonResponse({'status': 'error', 'message': 'Invalid symbol or API request failed'}, status=400)
        
        
        UserStock.objects.get_or_create(user=request.user, stock=symbol)
        
        return JsonResponse({'status': 'added', 'message': 'Stock added'}, status=201)

    def delete(self, request, format=None):
        # Delete a stock from the user's watchlist
    
        symbol = json.loads(request.data.get('symbol'))
        symbol_obj = SimpleNamespace(**symbol)
    
        if not symbol:
            return Response({'error': 'Symbol is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user_stock = UserStock.objects.get(user=request.user, stock=symbol_obj.symbol)
            user_stock.delete()
            return Response({'success': 'Stock deleted'}, status=status.HTTP_200_OK)

        except UserStock.DoesNotExist:
            return Response({'error': 'User does not have this stock'}, status=status.HTTP_404_NOT_FOUND)
        
        
@api_view(['GET'])
def user_view(request):
    user = request.user
    return Response({'username': user.username})

@csrf_exempt
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return JsonResponse({'status': 'success', 'message': 'Logged in successfully'})
    
@method_decorator(ensure_csrf_cookie, name='dispatch')
class GetCSRFToken(APIView):
    permission_classes = (permissions.AllowAny, )

    def get(self, request, format=None):
        print("cookie ensured")
        return Response({ 'success': 'CSRF cookie set' })
