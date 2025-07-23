from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal, ROUND_HALF_UP


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
    stock = models.IntegerField(validators=[MinValueValidator(0)], null=True,
                                default=1)
    first_created = models.DateField(auto_now_add=True)
    last_update= models.DateField(auto_now=True)

    def __str__(self):
        return self.name
    
    def time_length(self):
        """Returns when it was last updated."""
        return (self.last_update - self.first_created).days if self.first_created and self.last_update else 0


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
    stock = models.IntegerField(validators=[MinValueValidator(0)], null=True,
                                default=1)
    first_created = models.DateField(auto_now_add=True)
    last_update= models.DateField(auto_now=True, null=True)

    def __str__(self):
        return self.name
    
    def time_length(self):
        """Returns when it was last updated."""
        return (self.last_update - self.first_created).days if self.first_created and self.last_update else 0


class Product(models.Model):
    """Creates the Product Model."""
    name = models.CharField(max_length=50)
    stock = models.IntegerField(null=True, blank=True,
                                default=0)
    calculated_price = models.DecimalField(max_digits=10, decimal_places=2,
                                           null=True, blank=True,
                                           default=Decimal("0.00"))
    retail_price = models.DecimalField(max_digits=10, decimal_places=2,
                                       null=True, blank=True,
                                       default=Decimal("0.00"))
    product_margin = models.DecimalField(max_digits=10, decimal_places=2)
    labor_time = models.DecimalField(max_digits=10, decimal_places=2)
    miscellaneous_margin = models.DecimalField(max_digits=10, decimal_places=2)
    buffer = models.DecimalField(max_digits=10, decimal_places=2)
    first_created = models.DateField(auto_now_add=True)
    last_update= models.DateField(auto_now=True, null=True)
    
    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
    
    def time_length(self):
        """Returns when it was last updated."""
        return (self.last_update - self.first_created).days if self.first_created and self.last_update else 0
    

class ProductTextile(models.Model):
    """Creates the Product Textile Model."""
    textile = models.ForeignKey(Textile, on_delete=models.CASCADE,
                                related_name="textile")
    name = models.CharField(max_length=255, null=True,
                            blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name="products")
    height = models.DecimalField(max_digits=6, decimal_places=2,
                                       null=True, blank=True,
                                       default=0.00)
    width = models.DecimalField(max_digits=6, decimal_places=2,
                                       null=True, blank=True,
                                       default=0.00)
    quantity = models.IntegerField(validators=[MinValueValidator(0)])


class ProductAccessory(models.Model):
    """Creates the Product Accessory Model."""
    accessory = models.ForeignKey(Accessory, on_delete=models.CASCADE,
                                  related_name="accessory")
    name = models.CharField(max_length=255, null=True,
                            blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name="product")
    quantity = models.IntegerField(validators=[MinValueValidator(0)])


def compute_product_price(product):
    """Computes the calculated price of a product from its components with debug output."""
    textile_items = ProductTextile.objects.filter(product=product)
    textile_cost = Decimal("0.00")
    total_area = Decimal("0.00")

    print(f"\n📦 Computing textile cost for product: {product.name}")

    for item in textile_items:
        height = Decimal(item.height)
        width = Decimal(item.width)
        quantity = Decimal(item.quantity)
        cost_per_unit = Decimal(item.textile.cost)
        unit = item.textile.unit

        # Convert area to square feet
        area_in_sq_inches = height * width
        if unit == "FT":
            area_per_piece_sqft = area_in_sq_inches / Decimal("144")
        elif unit == "M":
            area_per_piece_sqft = area_in_sq_inches * Decimal("10.7639")
        else:  # INCH assumed
            area_per_piece_sqft = area_in_sq_inches / Decimal("144")

        line_area = area_per_piece_sqft * quantity
        total_area += line_area
        line_cost = line_area * cost_per_unit
        textile_cost += line_cost

        print(f"  - Textile: {item.textile.name}")
        print(f"    Dimensions (H x W): {height} in x {width} in")
        print(f"    Area per piece: {area_per_piece_sqft:.4f} sq ft")
        print(f"    Quantity: {quantity}")
        print(f"    Line area: {line_area:.4f} sq ft")
        print(f"    Unit Cost: {cost_per_unit}, Line Cost: {line_cost:.2f}")

    # Apply buffer after all items are processed
    buffer_multiplier = Decimal("1.00") + (Decimal(product.buffer) / Decimal("100"))
    buffered_area = total_area * buffer_multiplier
    textile_cost *= buffer_multiplier

    print(f"➡️ Total Area: {total_area:.4f} sq ft")
    print(f"➡️ Buffered Area (with {product.buffer}% buffer): {buffered_area:.4f} sq ft")
    print(f"💵 Textile Cost (with buffer): {textile_cost:.2f}")

    # Accessory cost
    accessory_items = ProductAccessory.objects.filter(product=product)
    accessory_cost = Decimal("0.00")
    
    for item in accessory_items:
        cost_per_unit = item.accessory.cost
        quantity = Decimal(item.quantity)
        accessory_cost += cost_per_unit * quantity

    print(f"💡 Accessory Cost: {accessory_cost:.2f}")

    # Total raw material
    raw_material_cost = textile_cost + accessory_cost

    # Base calculated price (pre-margin)
    raw_price = (
        raw_material_cost
        + Decimal(product.labor_time)
        + Decimal(product.miscellaneous_margin)
    )

    # Apply product margin as percentage
    margin_multiplier = Decimal("1.00") + (Decimal(product.product_margin) / Decimal("100"))
    calculated_price = raw_price * margin_multiplier
    calculated_price = calculated_price.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    print(f"🧾 Raw Price (before margin): {raw_price:.2f}\n")
    print(f"🧾 Calculated Price (after margin): {calculated_price:.2f}\n")

    return calculated_price


# Original Attempt
# def compute_product_price(product):
    """Computes the calculated price of a product from its components."""
    # Calculate total textile cost
    textile_items = ProductTextile.objects.filter(product=product)
    textile_cost = Decimal("0.00")
    
    for item in textile_items:
        area = Decimal(item.height) * Decimal(item.width)
        quantity = Decimal(item.quantity)
        cost_per_unit = Decimal(item.textile.cost)
        unit = item.textile.unit
        
        # Convert area based on unit
        if unit == "FT":
            area_in_sqft = area / Decimal("144")  # assuming inches to square feet
        elif unit == "M":
            area_in_sqft = area * Decimal("10.7639")  # assuming square meters to square feet
        else:  # "INCH"
            area_in_sqft = area

        textile_cost += cost_per_unit * area_in_sqft * Decimal(quantity)
        textile_cost *= product.buffer

    # Calculate total accessory cost
    accessory_items = ProductAccessory.objects.filter(product=product)
    accessory_cost = Decimal("0.00")
    
    for item in accessory_items:
        cost_per_unit = item.accessory.cost
        quantity = Decimal(item.quantity)
        accessory_cost += cost_per_unit * quantity

    # Total raw material cost
    raw_material_cost = textile_cost + accessory_cost

    # Apply pricing formula
    raw_price = (
        Decimal(raw_material_cost)
        + Decimal(product.labor_time)
        + Decimal(product.miscellaneous_margin))
    
    # Apply Product Margin
    calculated_price = (Decimal(raw_price)* (Decimal("1.00") + Decimal(product.product_margin)))

    # VAT = Decimal("0.12") * raw_price
    # SRP = Decimal(VAT + raw_price)
    
    # return SRP.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    return calculated_price.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


class Labor(models.Model):
    """Creates the Labor Model."""
    name = models.CharField(max_length=255, null=True,
                            blank=True)
    cost = models.DecimalField(max_digits=6, decimal_places=2,
                                 null=True, blank=True,
                                 default=0)
    unit = models.DecimalField(max_digits=6, decimal_places=2,
                                 null=True, blank=True,
                                 default=0)
    

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
