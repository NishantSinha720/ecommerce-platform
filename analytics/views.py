from django.db.models import Sum, Count
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from orders.models import Order
from products.models import Product
from inventory.models import Stock

@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def summary(request):
    confirmed = Order.objects.filter(status="CONFIRMED")
    revenue = confirmed.aggregate(v=Sum("total_amount"))["v"] or 0
    return Response({
        "products": Product.objects.filter(is_active=True).count(),
        "orders": confirmed.count(),
        "revenue": float(revenue),
        "stock_units": sum(x.quantity for x in Stock.objects.all()),
        "low_stock": sum(
            1 for x in Stock.objects.select_related("product")
            if x.available_quantity <= x.product.stock_alert_level
        ),
    })

@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def forecast(request):
    from sklearn.linear_model import LinearRegression
    import numpy as np

    rows = list(
        Order.objects.filter(status="CONFIRMED")
        .values("created_at")
        .annotate(count=Count("id"))
        .order_by("created_at")
    )
    if len(rows) < 2:
        return Response({
            "method": "linear_regression",
            "forecast_next": 0,
            "message": "Need at least two order dates for a forecast."
        })
    y = np.array([r["count"] for r in rows], dtype=float)
    X = np.arange(len(y)).reshape(-1, 1)
    model = LinearRegression().fit(X, y)
    prediction = max(0, float(model.predict([[len(y)]])[0]))
    return Response({
        "method": "linear_regression",
        "forecast_next": round(prediction, 2),
        "samples": len(y),
    })
