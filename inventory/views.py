from django.db import transaction
from django.db.models import F
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Warehouse, Stock, StockMovement
from .serializers import WarehouseSerializer, StockSerializer, StockMovementSerializer

class WarehouseViewSet(viewsets.ModelViewSet):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer
    permission_classes = [permissions.IsAuthenticated]

class StockViewSet(viewsets.ModelViewSet):
    queryset = Stock.objects.select_related("product", "warehouse").all()
    serializer_class = StockSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=["get"])
    def low_stock(self, request):
        items = [x for x in self.get_queryset() if x.available_quantity <= x.product.stock_alert_level]
        return Response(StockSerializer(items, many=True).data)

    @action(detail=False, methods=["get"])
    def available(self, request):
        items = [x for x in self.get_queryset() if x.available_quantity > 0]
        return Response(StockSerializer(items, many=True).data)

    @action(detail=True, methods=["post"])
    def stock_in(self, request, pk=None):
        return self._move(request, self.get_object(), "IN", request.data.get("quantity", 0))

    @action(detail=True, methods=["post"])
    def stock_out(self, request, pk=None):
        return self._move(request, self.get_object(), "OUT", request.data.get("quantity", 0))

    def _move(self, request, stock, movement_type, quantity):
        try:
            quantity = int(quantity)
        except (TypeError, ValueError):
            return Response({"detail": "quantity must be an integer"}, status=400)
        if quantity <= 0:
            return Response({"detail": "quantity must be positive"}, status=400)

        with transaction.atomic():
            stock = Stock.objects.select_for_update().get(pk=stock.pk)
            if movement_type == "OUT" and stock.available_quantity < quantity:
                return Response({"detail": "Insufficient available stock"}, status=400)
            if movement_type == "IN":
                stock.quantity = F("quantity") + quantity
            else:
                stock.quantity = F("quantity") - quantity
            stock.save(update_fields=["quantity", "updated_at"])
            stock.refresh_from_db()
            StockMovement.objects.create(
                stock=stock,
                movement_type=movement_type,
                quantity=quantity,
                reference=request.data.get("reference", ""),
                notes=request.data.get("notes", ""),
                created_by=request.user,
            )
        return Response(StockSerializer(stock).data)

    @action(detail=True, methods=["post"])
    def reserve(self, request, pk=None):
        quantity = int(request.data.get("quantity", 0))
        if quantity <= 0:
            return Response({"detail": "quantity must be positive"}, status=400)
        with transaction.atomic():
            stock = Stock.objects.select_for_update().get(pk=pk)
            if stock.available_quantity < quantity:
                return Response({"detail": "Insufficient available stock"}, status=400)
            stock.reserved_quantity += quantity
            stock.save(update_fields=["reserved_quantity", "updated_at"])
            StockMovement.objects.create(
                stock=stock, movement_type="RESERVE", quantity=quantity,
                created_by=request.user
            )
        return Response(StockSerializer(stock).data)

    @action(detail=True, methods=["post"])
    def release(self, request, pk=None):
        quantity = int(request.data.get("quantity", 0))
        if quantity <= 0:
            return Response({"detail": "quantity must be positive"}, status=400)
        with transaction.atomic():
            stock = Stock.objects.select_for_update().get(pk=pk)
            if stock.reserved_quantity < quantity:
                return Response({"detail": "Cannot release more than reserved"}, status=400)
            stock.reserved_quantity -= quantity
            stock.save(update_fields=["reserved_quantity", "updated_at"])
            StockMovement.objects.create(
                stock=stock, movement_type="RELEASE", quantity=quantity,
                created_by=request.user
            )
        return Response(StockSerializer(stock).data)

class StockMovementViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = StockMovement.objects.select_related("stock", "stock__product", "stock__warehouse").all()
    serializer_class = StockMovementSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_context(self):
        return {"request": self.request}
