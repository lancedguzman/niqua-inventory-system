from django.test import TestCase
from decimal import Decimal
from .models import accessory_compute, textile_compute, product_pricing


class AccessoryComputeTest(TestCase):
    """Unit test for accessory_compute."""
    def test_compute_total_cost(self):
        cost = Decimal("12.500")
        quantity = 4
        expected = Decimal("50.000")
        result = accessory_compute(cost, quantity)
        print(result)
        self.assertEqual(result, expected)

    def test_zero_quantity(self):
        cost = Decimal("10.000")
        quantity = 0
        expected = Decimal("0.000")
        result = accessory_compute(cost, quantity)
        print(result)
        self.assertEqual(result, expected)

    def test_zero_cost(self):
        cost = Decimal("0.000")
        quantity = 5
        expected = Decimal("0.000")
        result = accessory_compute(cost, quantity)
        print(result)
        self.assertEqual(result, expected)


class TextileComputeTest(TestCase):
    """Unit test for textile_compute."""
    def test_compute_total_cost(self):
        height = 8
        width = 2
        quantity = 2
        expected = 32
        result = textile_compute(height, width, quantity)
        print(result)
        self.assertEqual(result, expected)

    def test_zero_quantity(self):
        height = 10
        width = 5
        quantity = 0
        expected = 0
        result = textile_compute(height, width, quantity)
        print(result)
        self.assertEqual(result, expected)

    def test_zero_dimension(self):
        height = 0
        width = 5
        quantity = 10
        expected = 0
        result = textile_compute(height, width, quantity)
        print(result)
        self.assertEqual(result, expected)


class ProductPricingTest(TestCase):
    """Unit test for product_pricing."""
    def test_compute__product_pricing(self):
        material_price = textile_compute(2, 3, 5)
        accessory_price = accessory_compute(100, 3)
        product_margin = 100
        labor_time = 100
        miscellaneous_margin = 100
        buffer = 100
        expected = 1260
        result = product_pricing(
            product_margin, labor_time,
            miscellaneous_margin, buffer,
            material_price, accessory_price)
        print(result)
        self.assertEqual(result, expected)
