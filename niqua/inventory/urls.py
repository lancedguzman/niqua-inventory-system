from django.urls import path
from .views import *

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('base', base_template, name='base'),
    path('products/', product_list, name='product-list'),
    path('product/<int:product_id>/edit', product_edit, name='product-edit'),
    path('product/<int:product_id>/delete', product_delete, name='product-delete'),
    path('product/add/', product_form, name='product-form'),
    path('orders/', job_orders, name='order-list'),
    path('materials/', materials_list, name='material-list'),
    path('stock_in/', stock_list, name='stock-list'),
    path('reports/', report_list, name='report'),
]