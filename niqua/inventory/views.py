from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import transaction
from decimal import Decimal
from .models import Product, Accessory, Textile, Order
from .forms import *
from .models import compute_product_price


@login_required
def dashboard(request):
    """Displays the dashboard."""
    return render(request, "dashboard.html")


def product_list(request):
    """Displays the product list."""
    products = Product.objects.all()
    return render(request, "product_list.html",
                  {"products": products})


@transaction.atomic
def product_form(request):
    """Displays page to create a product along with associated textiles and accessories."""
    if request.method == "POST":
        product_form = ProductForm(request.POST)
        textile_formset = ProductTextileFormSet(request.POST, prefix="textile")
        accessory_formset = ProductAccessoryFormSet(request.POST, prefix="accessory")

        if product_form.is_valid() and textile_formset.is_valid() and accessory_formset.is_valid():
            # Save product without committing to DB yet
            product = product_form.save(commit=False)
            product.save()  # Save now to get a primary key (needed for formsets)

            # Assign product to formsets
            textile_formset.instance = product
            accessory_formset.instance = product

            # Save formsets
            textile_formset.save()
            accessory_formset.save()

            # Now that all related items are saved, compute the price
            product.calculated_price = compute_product_price(product)
            product.retail_price = (product.calculated_price * Decimal('1.12')).quantize(Decimal('0.01'))
            product.save()

            return redirect("product-list")

    else:
        product_form = ProductForm()
        textile_formset = ProductTextileFormSet(prefix="textile")
        accessory_formset = ProductAccessoryFormSet(prefix="accessory")

    return render(request, "product_form.html", {
        "product_form": product_form,
        "textile_formset": textile_formset,
        "accessory_formset": accessory_formset,
    })


def product_edit(request, product_id):
    """Displays page to edit products along with accessories and textiles."""
    product = Product.objects.get(id=product_id)

    if request.method == "POST":
        product_form = EditProductForm(request.POST, instance=product)
        textile_formset = ProductTextileFormSet(request.POST, instance=product, prefix="textile")
        accessory_formset = ProductAccessoryFormSet(request.POST, instance=product, prefix="accessory")

        if product_form.is_valid() and textile_formset.is_valid() and accessory_formset.is_valid():
            product_form.save()
            textile_formset.save()
            accessory_formset.save()
            return redirect("product-list")
    else:
        product_form = EditProductForm(instance=product)
        textile_formset = ProductTextileFormSet(instance=product, prefix="textile")
        accessory_formset = ProductAccessoryFormSet(instance=product, prefix="accessory")

    return render(request, "product_edit.html", {
        "edit_form": product_form,
        "textile_formset": textile_formset,
        "accessory_formset": accessory_formset,
    })


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