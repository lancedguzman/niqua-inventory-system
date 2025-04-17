from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator


class Profile(models.Model):
    """Creates the Profile Model."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, null=False)


class MaterialKey(models.Model):
    """Creates the Material Key."""
    material_key = models.AutoField(primary_key=True)


class Textile(models.Model):
    """Creates the Textile Model."""
    UNIT_CHOICES = [
        ("FT", "per sq/ft"),
        ("INCH", "per sq/inch"),
        ("M", "per sq/m"),
    ]
    name = models.CharField(max_length=50)
    cost = models.DecimalField(max_digits=6, decimal_places=3)
    unit = models.CharField(max_length=4, choices=UNIT_CHOICES,
                            default="FT")
    stock = models.IntegerField(validators=[MinValueValidator(0)])
    material_key = models.OneToOneField(MaterialKey, on_delete=models.CASCADE)


class Accessory(models.Model):
    """Creates the Accessory Model."""
    UNIT_CHOICES = [
        ("PC", "per piece"),
        ("INCH", "per inch"),
    ]

    name = models.CharField(max_length=50)
    cost = models.DecimalField(max_digits=6, decimal_places=3)
    unit = models.CharField(max_length=4, choices=UNIT_CHOICES,
                            default="PC")
    stock = models.IntegerField(validators=[MinValueValidator(0)])
    material_key = models.OneToOneField(MaterialKey, on_delete=models.CASCADE)


class Product(models.Model):
    """Creates the Product Model."""
    name = models.CharField(max_length=50)
    quantity = models.IntegerField()
    product_margin = models.DecimalField(max_digits=6, decimal_places=2)
    labor_time = models.DecimalField(max_digits=6, decimal_places=2)
    miscellaneous_margin = models.DecimalField(max_digits=6, decimal_places=2)
    retail_price = models.DecimalField(max_digits=6, decimal_places=2)
    calculated_price = models.DecimalField(max_digits=6, decimal_places=2)
    last_updated = models.DateField(auto_now_add=True)

    textiles = models.ManyToManyField(Textile, through="Product_Component")
    accessories = models.ManyToManyField(Accessory, through="Product_Accessory")
    
    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
    

class Component(models.Model):
    name = models.CharField(max_length=50)


class Product_Component(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    textile = models.ForeignKey(Textile, on_delete=models.CASCADE)
    component = models.ForeignKey(Component, on_delete=models.CASCADE)
    height = models.DecimalField(max_digits=6, decimal_places=2)
    width = models.DecimalField(max_digits=6, decimal_places=2)
    quantity = models.IntegerField(validators=[MinValueValidator(0)])
    buffer = models.DecimalField(max_digits=6, decimal_places=2)


class Product_Accessory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    accessory = models.ForeignKey(Accessory, on_delete=models.CASCADE)
    amount = models.IntegerField(validators=[MinValueValidator(0)])
