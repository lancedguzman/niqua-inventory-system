from django.contrib import admin
from django.contrib.auth.models import User
from .models import *


class ProfileInline(admin.StackedInline):
    """Creates the Profile Admin Panel."""
    model = Profile
    can_delete = False
    field = ["name"]


class UserAdmin(admin.ModelAdmin):
    """Sets how Profiles are displayed in Admin Panel."""
    inlines = [ProfileInline]


class ProductAdmin(admin.ModelAdmin):
    """Creates the Product Admin Panel."""
    model = Product
    list_display = ('name','stock',
                    'retail_price', 'calculated_price',
                    'product_margin', 'labor_time',
                    'miscellaneous_margin', 'first_created',
                    'buffer', 'last_update',)


class TextileAdmin(admin.ModelAdmin):
    """Creates the Textile Admin Panel."""
    model = Textile
    list_display = ('name', 'cost',
                    'unit','stock',
                    'first_created', 'last_update',)


class AccessoryAdmin(admin.ModelAdmin):
    """Creates the Accessory Admin Panel."""
    model = Accessory
    list_display = ('name', 'cost',
                    'unit','stock',
                    'first_created', 'last_update',)


class ProductTextileAdmin(admin.ModelAdmin):
    """Creates the ProductTextile Admin Panel."""
    model = ProductTextile
    list_display = ('textile', 'product',
                    'height', 'width',
                    'quantity',)


class ProductAccessoryAdmin(admin.ModelAdmin):
    """Creates the ProductAccessory Admin Panel."""
    model = ProductAccessory
    list_display = ('accessory', 'product',
                    'quantity',)
    

class LaborAdmin(admin.ModelAdmin):
    """Creates the Labor Admin Panel."""
    model = Labor
    list_display = ('name', 'cost', 'unit')


class OrderAdmin(admin.ModelAdmin):
    """Creates the Order Admin Panel."""
    model = Order
    list_display = ('customer', 'product',
                    'quantity', 'outlet',
                    'status',)


admin.site.register(Product, ProductAdmin)

admin.site.register(Textile, TextileAdmin)

admin.site.register(Accessory, AccessoryAdmin)

admin.site.register(ProductTextile, ProductTextileAdmin)

admin.site.register(ProductAccessory, ProductAccessoryAdmin)

admin.site.register(Labor, LaborAdmin)

admin.site.register(Order, OrderAdmin)

admin.site.unregister(User)

admin.site.register(User, UserAdmin)
