from django import forms
from .models import Product, Textile, Accessory, Order


class ProductForm(forms.ModelForm):
    """Form to create new products."""
    class Meta:
        model = Product
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to all fields
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})


class EditProductForm(forms.ModelForm):
    """Creates form to edit products."""
    class Meta:
        model = Product
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to all fields
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})


class TextileForm(forms.ModelForm):
    """Form to create new Textile."""
    class Meta:
        model = Textile
        fields = ["name", "cost",
                  "unit", "stock",]
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to all fields
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})


class AccessoryForm(forms.ModelForm):
    """Form to create new Textile."""
    class Meta:
        model = Accessory
        fields = ["name", "cost",
                  "unit", "stock",]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to all fields
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
        # Add Bootstrap classes to all fields
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
