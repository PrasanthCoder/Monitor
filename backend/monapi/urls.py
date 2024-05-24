# monapi/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('user_stocks/', views.user_stocks_view.as_view(), name='user_stocks'),
    path('user/', views.user_view, name='user_view'),
    path('logout/', views.logout_view, name='logout_view'),
    path('csrf_cookie/', views.GetCSRFToken.as_view()),
]
