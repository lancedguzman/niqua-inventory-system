from django.contrib import admin
from django.contrib.auth.models import User
from .models import Product, Profile, Textile, Accessory, ProductTextile, ProductAccessory


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
                    'miscellaneous_margin', 'last_updated')


class TextileAdmin(admin.ModelAdmin):
    """Creates the Textile Admin Panel."""
    model = Textile
    list_display = ('name', 'cost',
                    'unit','stock',)


class AccessoryAdmin(admin.ModelAdmin):
    """Creates the Accessory Admin Panel."""
    model = Accessory
    list_display = ('name', 'cost',
                    'unit','stock',)


class ProductTextileAdmin(admin.ModelAdmin):
    """Creates the ProductTextile Admin Panel."""
    model = ProductTextile
    list_display = ('name', 'stock',)


class ProductAccessoryAdmin(admin.ModelAdmin):
    """Creates the ProductAccessory Admin Panel."""
    model = ProductAccessory
    list_display = ('name', 'stock',)


admin.site.register(Product, ProductAdmin)

admin.site.register(Textile, TextileAdmin)

admin.site.register(Accessory, AccessoryAdmin)

admin.site.register(ProductTextile, ProductTextileAdmin)

admin.site.register(ProductAccessory, ProductAccessoryAdmin)

admin.site.unregister(User)

admin.site.register(User, UserAdmin)
