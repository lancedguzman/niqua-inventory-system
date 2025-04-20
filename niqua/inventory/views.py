from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product, Accessory, Textile, Order
from .forms import *

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
    """Displays page to create product."""
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
        form = EditProductForm(request.POST, instance=product)

        if form.is_valid():
            form.save()
            return redirect("product-list")
    
    else:
        form = EditProductForm(instance=product)

    return render(request, "product_edit.html",
                  {"edit_form": form})


def product_delete(request, product_id):
    """Deletes a product from product list."""
    product = Product.objects.get(id=product_id)
    product.delete()
    return redirect("product-list")


def job_orders(request):
    """Displays the current job orders."""
    orders = Order.objects.all()
    return render(request, "job_orders.html",
                  {"orders": orders})


def order_form(request):
    """Displays page to create job orders."""
    if (request.method == "POST"):
        form = OrderForm(request.POST)

        if form.is_valid():
            order = form.save()
            return redirect("order-list")
    else:
        form = OrderForm()

    return render(request, "order_form.html",
                  {"create_form": form})


def order_edit(request, pk):
    """Displays page to edit orders."""
    order = Order.objects.get(pk=pk)

    if (request.method == "POST"):
        form = EditOrderForm(request.POST, instance=order)

        if form.is_valid():
            form.save()
            return redirect("order-list")
    
    else:
        form = EditOrderForm(instance=order)

    return render(request, "order_edit.html",
                  {"edit_form": form})


def order_delete(request, pk):
    """Deletes a job order from the list."""
    order = Order.objects.get(pk=pk)
    order.delete()
    return redirect("order-list")


def material_list(request):
    """Displays the list of available materials."""
    textiles = Textile.objects.all()
    accessories = Accessory.objects.all()
    return render(request, "material_list.html", {
        "textiles": textiles,
        "accessories": accessories,
    })


def material_form(request, material_type):
    """Displays form to add material."""
    model_map = {
        "textile": (Textile, TextileForm),
        "accessory": (Accessory, AccessoryForm),
    }

    model_form_pair = model_map.get(material_type.lower())
    model, form_class = model_form_pair

    if (request.method == "POST"):
        form = form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect("material-list")
        
    else:
        form = form_class()

    return render(request, "material_form.html", {
        "create_form": form,
        "material_type": material_type,
    })


def material_edit(request, material_type, pk):
    """Displays form to edit material."""
    model_map = {
        "textile": (Textile, EditTextileForm),
        "accessory": (Accessory, EditAccessoryForm),
    }

    model_form_pair = model_map.get(material_type.lower())
    model, form_class = model_form_pair
    instance = model.objects.filter(pk=pk).first()

    if (request.method == "POST"):
        form = form_class(request.POST, instance=instance)

        if form.is_valid():
            form.save()
            return redirect("material-list")
        
    else:
        form = form_class(instance=instance)

    return render(request, "material_edit.html", {
        "edit_form": form,
        "material_type": material_type,
    })


def material_delete(request, material_type, pk):
    """Delete a material from material list."""
    model_map = {
        "textile": Textile,
        "accessory": Accessory,
    }

    model = model_map.get(material_type.lower())
    material = get_object_or_404(model, pk=pk)
    material.delete()

    return redirect("material-list")


def stock_list(request):
    """Displays the current stock in inventory."""
    return render(request, "stock_list.html")


def report_list(request):
    """Displays the report list page."""
    return render(request, "report_list.html")


def base_template(request):
    """Displays the base template."""
    return render(request, "base.html")