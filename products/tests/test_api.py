from django.test import TestCase
from rest_framework.test import APIClient

from products.models import Product, Category


class ProductAPITest(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.category = Category.objects.create(
            name="Test Category"
        )

        self.product = Product.objects.create(
            name="Test Product",
            sku="TEST-001",
            description="Test product",
            price=100,
            category=self.category,
            stock_alert_level=5,
            is_active=True,
        )

    def test_product_list(self):
        response = self.client.get("/api/products/")
        self.assertEqual(response.status_code, 200)

    def test_category_list(self):
        response = self.client.get("/api/categories/")
        self.assertEqual(response.status_code, 200)

    def test_product_detail(self):
        response = self.client.get(
            f"/api/products/{self.product.id}/"
        )
        self.assertEqual(response.status_code, 200)
