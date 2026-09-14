from django.conf import settings
from django.db import models
from products.models import Product

class Warehouse(models.Model):
    name = models.CharField(max_length=150)
    code = models.CharField(max_length=50, unique=True)
    address = models.TextField(blank=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.code})"

class Stock(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="stocks")
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name="stocks")
    quantity = models.PositiveIntegerField(default=0)
    reserved_quantity = models.PositiveIntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["product", "warehouse"], name="unique_product_warehouse"
            )
        ]

    @property
    def available_quantity(self):
        return max(0, self.quantity - self.reserved_quantity)

class StockMovement(models.Model):
    TYPES = [
        ("IN", "Stock In"),
        ("OUT", "Stock Out"),
        ("ADJUSTMENT", "Adjustment"),
        ("RESERVE", "Reserve"),
        ("RELEASE", "Release"),
    ]
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name="movements")
    movement_type = models.CharField(max_length=20, choices=TYPES)
    quantity = models.PositiveIntegerField()
    reference = models.CharField(max_length=150, blank=True)
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL
    )
    created_at = models.DateTimeField(auto_now_add=True)
