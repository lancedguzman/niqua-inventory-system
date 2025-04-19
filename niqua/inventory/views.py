from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Product
from .forms import ProductForm, EditForm

@login_required
def dashboard(request):
    """Displays the dashboard."""
    return render(request, "dashboard.html")


def product_list(request):
    """Displays the product list."""
    products = Product.objects.all()
    return render(request, "product_list.html",
                  {"products": products})


def product_form(request):
    """Handles product creation."""
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save()
            return redirect("product-list")
    else:
        form = ProductForm()

    return render(request, "product_form.html",
                  {"product_form": form})


def product_edit(request, product_id):
    """Displays page to edit products."""
    product = Product.objects.get(id=product_id)

    if (request.method == "POST"):
        form = EditForm(request.POST, instance=product)

        if form.is_valid():
            form.save()
            return redirect("product-list")
    
    else:
        form = EditForm(instance=product)

    return render(request, "product_edit.html",
                  {"edit_form": form})


def product_delete(request, product_id):
    """Deletes a product from product list."""
    product = Product.objects.get(id=product_id)
    product.delete()
    return redirect("product-list")


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