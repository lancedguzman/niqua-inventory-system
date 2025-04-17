from django.contrib import admin
from django.contrib.auth.models import User
from .models import Product, Profile


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


admin.site.register(Product, ProductAdmin)

admin.site.unregister(User)

admin.site.register(User, UserAdmin)
