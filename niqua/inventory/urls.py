from django.urls import path
from .views import *

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('base', base_template, name='base'),
    path('products/', product_list, name='product-list'),
    path('orders/', job_orders, name='order-list'),
    path('materials/', materials_list, name='material-list'),
    path('stock_in/', stock_list, name='stock-list'),
    path('reports/', report_list, name='report'),
]