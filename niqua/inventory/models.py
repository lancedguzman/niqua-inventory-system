from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal


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
    stock = models.IntegerField(null=True, blank=True,
                                default=0)
    calculated_price = models.DecimalField(max_digits=6, decimal_places=2,
                                           null=True, blank=True,
                                           default=0)
    retail_price = models.DecimalField(max_digits=6, decimal_places=2,
                                       null=True, blank=True,
                                       default=0)
    product_margin = models.DecimalField(max_digits=6, decimal_places=2)
    labor_time = models.DecimalField(max_digits=6, decimal_places=2)
    miscellaneous_margin = models.DecimalField(max_digits=6, decimal_places=2)
    buffer = models.DecimalField(max_digits=6, decimal_places=2)
    last_updated = models.DateField(auto_now=True)
    
    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
    

def textile_compute(height, width, quantity):
    """Gets the total cost of textiles used."""
    material_price = height * width * quantity
    return material_price


def accessory_compute(cost, quantity):
    """Gets the total cost of accessories used."""
    accessory_price = cost * quantity
    return accessory_price


def product_pricing(product_margin, labor_time,
                    miscellaneous_margin, buffer):
    """Gets the calculated price of the product."""
    raw_material = textile_compute + accessory_compute
    estimated_selling = (raw_material
               + labor_time
               + product_margin
               + miscellaneous_margin
               * buffer)
    return estimated_selling


def compute_product_price(product):
    """Computes the calculated price of a product from its components."""
    # Calculate total textile cost
    textile_items = ProductTextile.objects.filter(product=product)
    textile_cost = Decimal("0.00")
    
    for item in textile_items:
        area = Decimal(item.height) * Decimal(item.width)
        quantity = Decimal(item.quantity)
        cost_per_unit = item.textile.cost
        unit = item.textile.unit
        
        # Convert area based on unit
        if unit == "FT":
            area_in_sqft = area / Decimal("144")  # assuming inches to square feet
        elif unit == "M":
            area_in_sqft = area * Decimal("10.7639")  # assuming square meters to square feet
        else:  # "INCH"
            area_in_sqft = area

        textile_cost += cost_per_unit * area_in_sqft * quantity

    # Calculate total accessory cost
    accessory_items = ProductAccessory.objects.filter(product=product)
    accessory_cost = Decimal("0.00")
    
    for item in accessory_items:
        cost_per_unit = item.accessory.cost
        quantity = Decimal(item.quantity)
        accessory_cost += cost_per_unit * quantity

    # Total raw material cost
    raw_material_cost = textile_cost + accessory_cost

    # Apply final pricing formula
    calculated_price = (
        raw_material_cost
        + product.labor_time
        + product.product_margin
        + product.miscellaneous_margin
    ) * product.buffer

    return calculated_price.quantize(Decimal("0.01"))
    

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
