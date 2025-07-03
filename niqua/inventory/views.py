from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import transaction
from decimal import Decimal
from collections import defaultdict
from .models import Product, Accessory, Textile, Order, Labor
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
    """Displays page to create a product along with grouped textiles and accessories."""
    if request.method == "POST":
        product_form = ProductForm(request.POST)
        accessory_formset = ProductAccessoryFormSet(request.POST, prefix="accessory")

        # Extract flat textile POST data
        textile_formset = ProductTextileFormSet(request.POST, prefix="textile")

        try:
            for i, form in enumerate(ProductTextileFormSet(request.POST, prefix="textile")):
                print(f"Textile form {i} POST value:", form.data.get(f"textile-{i}-textile"))
            for key in request.POST:
                print(f"{key}: {request.POST[key]}")

            if product_form.is_valid() and textile_formset.is_valid() and accessory_formset.is_valid():
                product = product_form.save(commit=False)
                product.save()

                # Save accessories
                accessory_formset.instance = product
                accessory_formset.save()

                # Group textile forms by textile field
                grouped = defaultdict(list)
                for form in textile_formset:
                    textile = form.cleaned_data.get("textile")
                    if textile:
                        grouped[textile].append(form)

                for textile, forms in grouped.items():
                    for form in forms:
                        instance = form.save(commit=False)
                        instance.product = product
                        instance.textile = textile
                        instance.save()

                # Calculate price
                product.calculated_price = Decimal(compute_product_price(product))
                product.retail_price = Decimal((product.calculated_price * Decimal('1.12')).quantize(Decimal('0.01')))
                product.save()

                return redirect("product-list")
            else:
                print("Form errors:", product_form.errors, textile_formset.errors, accessory_formset.errors)

        except Exception as e:
            import traceback
            traceback.print_exc()
            print("Exception during save:", e)

    else:
        product_form = ProductForm()
        textile_formset = ProductTextileFormSet(prefix="textile")
        accessory_formset = ProductAccessoryFormSet(prefix="accessory")

    return render(request, "product_form.html", {
        "product_form": product_form,
        "textile_formset": textile_formset,  # still a flat formset in HTML
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


def labor_list(request):
    """Displays list of labor cost."""
    labors = Labor.objects.all()
    return render(request, "labor_list.html",
                  {"labors": labors})


def labor_form(request):
    """Displays form to edit labor."""
    if (request.method == "POST"):
        form = LaborForm(request.POST)

        if form.is_valid():
            labor = form.save(commit=False)

            if labor.cost:
                labor.unit = (labor.cost / (Decimal('8')) / Decimal('60'))
            labor.save()
            return redirect("labor-list")
        
    else:
        form = LaborForm()

    return render(request, "labor_form.html",
                  {"labor_form": form})


def labor_edit(request, pk):
    """Displays form to edit labor."""   
    labor = Labor.objects.get(pk=pk)
    
    if (request.method == "POST"):
        labor_form = EditLaborForm(request.POST, instance=labor)

        if labor_form.is_valid():
            labor_form.save(commit=False)
            if labor.cost:
                labor.unit = (labor.cost / (Decimal('8')) / Decimal('60'))
            labor.save()
            return redirect("labor-list")

    else:
        labor_form = EditLaborForm(instance=labor)

    return render(request, "labor_edit.html", {
        "edit_form": labor_form
    })


def labor_delete(request, pk):
    """Delete labor from the list."""
    labor = Labor.objects.get(pk=pk)
    labor.delete()
    return redirect("labor-list")


def stock_list(request):
    """Displays the current stock in inventory."""
    products = Product.objects.all()
    return render(request, "stock_list.html",
                  {"products": products})


def report_list(request):
    """Displays the report list page."""
    return render(request, "report_list.html")


def base_template(request):
    """Displays the base template."""
    return render(request, "base.html")