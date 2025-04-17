from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Product

@login_required
def dashboard(request):
    """Displays the dashboard."""
    return render(request, "dashboard.html")


def product_list(request):
    """Displays the product list."""
    products = Product.objects.all()
    return render(request, "product_list.html",
                  {"products": products})

def job_orders(request):
    """Displays the current job orders."""
    return render(request, "job_orders.html")


def materials_list(request):
    """Displays the list of available materials."""
    return render(request, "materials_list.html")


def stock_list(request):
    """Displays the current stock in inventory."""
    return render(request, "stock_list.html")


def report_list(request):
    """Displays the report list page."""
    return render(request, "report_list.html")


def base_template(request):
    """Displays the base template."""
    return render(request, "base.html")