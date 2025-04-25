from django import forms
from django.forms import inlineformset_factory
from .models import *


class ProductForm(forms.ModelForm):
    """Form to create new products."""
    class Meta:
        model = Product
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

        self.fields['retail_price'].widget.attrs['readonly'] = True
        self.fields['calculated_price'].widget.attrs['readonly'] = True


class EditProductForm(forms.ModelForm):
    """Creates form to edit products."""
    class Meta:
        model = Product
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})


class TextileForm(forms.ModelForm):
    """Form to create new Textile."""
    class Meta:
        model = Textile
        fields = ["name", "cost", "unit", "stock"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})


class AccessoryForm(forms.ModelForm):
    """Form to create new Accessory."""
    class Meta:
        model = Accessory
        fields = ["name", "cost", "unit", "stock"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})


# -----------------------------
# Inline Formsets with styling
# -----------------------------

class ProductTextileInlineForm(forms.ModelForm):
    """Inline form for ProductTextile"""
    class Meta:
        model = ProductTextile
        fields = ['textile', 'height',
                  'width', 'quantity']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})


class ProductAccessoryInlineForm(forms.ModelForm):
    """Inline form for ProductAccessory"""
    class Meta:
        model = ProductAccessory
        fields = ['accessory', 'quantity']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})


# -----------------------------
# Inline Formset Factories
# -----------------------------


ProductTextileFormSet = inlineformset_factory(
    Product, ProductTextile,
    form=ProductTextileInlineForm,
    fields=['textile', 'height',
            'width', 'quantity'],
    extra=1, can_delete=False # CHANGE
)

ProductAccessoryFormSet = inlineformset_factory(
    Product, ProductAccessory,
    form=ProductAccessoryInlineForm,
    fields=['accessory', 'quantity'],
    extra=1, can_delete=False # CHANGE
)


class OrderForm(forms.ModelForm):
    """Form to create job orders."""
    class Meta:
        model = Order
        fields = "__all__"
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to all fields
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'}) 


class EditOrderForm(forms.ModelForm):
    """Creates form to edit order."""
    class Meta:
        model = Order
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to all fields
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'}) 
