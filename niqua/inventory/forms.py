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

        # Optional fields (calculated post-save)
        self.fields['retail_price'].widget.attrs['readonly'] = True
        self.fields['calculated_price'].widget.attrs['readonly'] = True
        self.fields['retail_price'].required = False
        self.fields['calculated_price'].required = False
        self.fields['stock'].required = False


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


class EditTextileForm(forms.ModelForm):
    """Creates form to edit Textile."""
    class Meta:
        model = Textile
        fields = ["name", "cost",
                  "unit", "stock",]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})


class EditAccessoryForm(forms.ModelForm):
    """Creates form to edit Textile."""
    class Meta:
        model = Accessory
        fields = ["name", "cost",
                  "unit", "stock",]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to all fields
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})


class LaborForm(forms.ModelForm):
    """Form to create labor."""
    class Meta:
        model = Labor
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

        self.fields['unit'].widget.attrs['readonly'] = True
        self.fields['unit'].required = False


class EditLaborForm(forms.ModelForm):
    """Form to edit labor."""
    class Meta:
        model = Labor
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

        self.fields['unit'].widget.attrs['readonly'] = True
        self.fields['unit'].required = False


# -----------------------------
# Inline Formsets with styling
# -----------------------------

class ProductTextileInlineForm(forms.ModelForm):
    """Inline form for a single textile detail row."""
    class Meta:
        model = ProductTextile
        fields = ['textile', 'name', 'height', 'width', 'quantity']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Hide the textile field (handled via shared dropdown)
        self.fields['textile'].widget = forms.HiddenInput()
        self.fields['textile'].widget.attrs.update({
            'class': 'form-control textile-id-input'
        })

        # Add form-control class to all other fields
        for field_name in ['name', 'height', 'width', 'quantity']:
            self.fields[field_name].widget.attrs.update({
                'class': 'form-control'
            })


class ProductAccessoryInlineForm(forms.ModelForm):
    """Inline form for ProductAccessory"""
    class Meta:
        model = ProductAccessory
        fields = ['accessory', 'name', 'quantity']

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
    extra=1,
    can_delete=False
)


ProductAccessoryFormSet = inlineformset_factory(
    Product, ProductAccessory,
    form=ProductAccessoryInlineForm,
    extra=1,
    can_delete=False
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
