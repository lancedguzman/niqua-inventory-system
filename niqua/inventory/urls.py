from django.urls import path
from .views import *

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('base', base_template, name='base'),
    path('products/', product_list, name='product-list'),
    path('product/add/', product_form, name='product-form'),
    path('product/<int:product_id>/edit', product_edit, name='product-edit'),
    path('product/<int:product_id>/delete', product_delete, name='product-delete'),
    path('orders/', job_orders, name='order-list'),
    path('materials/', material_list, name='material-list'),
    path('material/<str:material_type>/add/', material_form, name='material-form'),
    path('material/<str:material_type>/<int:pk>/edit', material_edit, name='material-edit'),
    path('material/<str:material_type>/<int:pk>/delete', material_delete, name='material-delete'),
    path('stock_in/', stock_list, name='stock-list'),
    path('reports/', report_list, name='report'),
]