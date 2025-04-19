from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator


class Profile(models.Model):
    """Creates the Profile Model."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, null=False)


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

    def __str__(self):
        return self.name


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

    def __str__(self):
        return self.name


class Product(models.Model):
    """Creates the Product Model."""
    name = models.CharField(max_length=50)
    stock = models.IntegerField()
    retail_price = models.DecimalField(max_digits=6, decimal_places=2)
    calculated_price = models.DecimalField(max_digits=6, decimal_places=2)
    product_margin = models.DecimalField(max_digits=6, decimal_places=2)
    labor_time = models.DecimalField(max_digits=6, decimal_places=2)
    miscellaneous_margin = models.DecimalField(max_digits=6, decimal_places=2)
    last_updated = models.DateField(auto_now=True)

    # textiles = models.ManyToManyField(Textile, through="ProductTextile")
    # accessories = models.ManyToManyField(Accessory, through="ProductAccessory")
    
    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
    

class ProductTextile(models.Model):
    """Creates the Product Textile Model."""
    textile = models.ForeignKey(Textile, on_delete=models.CASCADE,
                                related_name="textile")
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name="products")
    name = models.CharField(max_length=255)
    stock = models.IntegerField(validators=[MinValueValidator(0)])

    def __str__(self):
        return self.name


class ProductAccessory(models.Model):
    """Creates the Product Accessory Model."""
    accessory = models.ForeignKey(Accessory, on_delete=models.CASCADE,
                                  related_name="accessory")
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name="product")
    name = models.CharField(max_length=255)
    stock = models.IntegerField(validators=[MinValueValidator(0)])

    def __str__(self):
        return self.name
