from django.test import TestCase

from products.models import Product, Category
from inventory.models import Warehouse, Stock


class InventoryModelTest(TestCase):

    def test_stock_creation(self):
        category = Category.objects.create(
            name="Inventory Test"
        )

        product = Product.objects.create(
            name="Inventory Product",
            sku="INV-001",
            price=50,
            category=category,
        )

        warehouse = Warehouse.objects.create(
            name="Test Warehouse",
            code="TEST"
        )

        stock = Stock.objects.create(
            product=product,
            warehouse=warehouse,
            quantity=10,
            reserved_quantity=0,
        )

        self.assertEqual(stock.quantity, 10)
        self.assertEqual(stock.available_quantity, 10)
