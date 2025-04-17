from django.urls import path
from django.shortcuts import redirect

urlpatterns = [
    path('profile/', lambda request: redirect('login'))
]
