import os
import time

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django
django.setup()

from django.contrib.auth import get_user_model
from products.models import Category, Product
from inventory.models import Warehouse, Stock

User = get_user_model()

username = "admin"
password = "nishant123"
email = "admin@example.com"

user, _ = User.objects.get_or_create(
    username=username,
    defaults={"email": email, "is_staff": True, "is_superuser": True, "is_active": True},
)
user.email = email
user.is_staff = True
user.is_superuser = True
user.is_active = True
user.set_password(password)
user.save()

category, _ = Category.objects.get_or_create(
    name="Electronics",
    defaults={"description": "Default electronics category"},
)

products = [
    ("Demo Laptop", "DEMO-LAPTOP-001", "Business laptop demo product", 75000, 5, 20),
    ("Demo Wireless Mouse", "DEMO-MOUSE-001", "Wireless mouse demo product", 2500, 10, 50),
]

warehouse, _ = Warehouse.objects.get_or_create(
    code="MAIN",
    defaults={"name": "Main Warehouse", "address": "India"},
)

for name, sku, desc, price, alert, qty in products:
    product, _ = Product.objects.get_or_create(
        sku=sku,
        defaults={
            "category": category,
            "name": name,
            "description": desc,
            "price": price,
            "stock_alert_level": alert,
            "is_active": True,
        },
    )
    Stock.objects.get_or_create(
        product=product,
        warehouse=warehouse,
        defaults={"quantity": qty},
    )

print("Bootstrap complete")
print("Login:", username, password)

