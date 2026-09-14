from rest_framework import serializers
from .models import Warehouse, Stock, StockMovement

class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = "__all__"

class StockSerializer(serializers.ModelSerializer):
    available_quantity = serializers.IntegerField(read_only=True)
    product_name = serializers.CharField(source="product.name", read_only=True)
    warehouse_name = serializers.CharField(source="warehouse.name", read_only=True)

    class Meta:
        model = Stock
        fields = (
            "id", "product", "product_name", "warehouse", "warehouse_name",
            "quantity", "reserved_quantity", "available_quantity", "updated_at"
        )

class StockMovementSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockMovement
        fields = "__all__"
        read_only_fields = ("created_by",)
