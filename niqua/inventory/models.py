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
    buffer = models.DecimalField(max_digits=6, decimal_places=2)
    last_updated = models.DateField(auto_now=True)
    
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
    height = models.IntegerField(validators=[MinValueValidator(0)])
    width = models.IntegerField(validators=[MinValueValidator(0)])
    quantity = models.IntegerField(validators=[MinValueValidator(0)])


class ProductAccessory(models.Model):
    """Creates the Product Accessory Model."""
    accessory = models.ForeignKey(Accessory, on_delete=models.CASCADE,
                                  related_name="accessory")
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name="product")
    quantity = models.IntegerField(validators=[MinValueValidator(0)])


class Order(models.Model):
    """Creates the Order Model."""
    STATUS_CHOICES = [
        ("INQ", "In-Queue"),
        ("COMP", "Completed"),
        ("CANC", "Cancelled"),
        ("INP", "In-Progress"),
    ]

    OUTLET_CHOICES = [
        ("ES", "Estancia"),
        ("CC", "Commerce Center"),
        ("GH", "Gray House"),
        ("OL", "Online"),
    ]
    customer = models.CharField(max_length=255)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(validators=[MinValueValidator(0)])
    outlet = models.CharField(choices=OUTLET_CHOICES)
    status = models.CharField(choices=STATUS_CHOICES)
    start_date = models.DateField()
    file_date = models.DateField()
    completion_date = models.DateField(null=True)

    def __str__(self):
        return self.customer


def textile_compute(height, width,
                    quantity):
    """Gets the total cost of textiles used."""
    material_price = (height
                    * width
                    * quantity)
    return material_price


def accessory_compute(cost, quantity):
    """Gets the total cost of accessories used."""
    accessory_price = cost * quantity
    return accessory_price


def product_pricing(product_margin, labor_time,
                    miscellaneous_margin, buffer):
    """Gets the calculated price of the product."""
    raw_material = textile_compute + accessory_compute
    estimated_selling = ((raw_material
               + labor_time
               + product_margin
               + miscellaneous_margin)
               / (1 + buffer))
    VAT = 700
    srp = estimated_selling + VAT
    return srp
