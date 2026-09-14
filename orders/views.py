from django.db import transaction
from django.db.models import Prefetch
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from inventory.models import Stock, StockMovement
from .models import Cart, CartItem, Order, OrderItem
from .serializers import CartSerializer, OrderSerializer

class CartViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def _cart(self, user):
        cart, _ = Cart.objects.get_or_create(user=user)
        return cart

    def list(self, request):
        return Response(CartSerializer(self._cart(request.user)).data)

    @action(detail=False, methods=["post"])
    def add(self, request):
        product_id = request.data.get("product")
        quantity = int(request.data.get("quantity", 1))
        if not product_id or quantity <= 0:
            return Response({"detail": "product and positive quantity are required"}, status=400)
        item, created = CartItem.objects.get_or_create(
            cart=self._cart(request.user),
            product_id=product_id,
            defaults={"quantity": quantity},
        )
        if not created:
            item.quantity += quantity
            item.save(update_fields=["quantity"])
        return Response(CartSerializer(item.cart).data)

    @action(detail=False, methods=["post"])
    def remove(self, request):
        CartItem.objects.filter(
            cart=self._cart(request.user), product_id=request.data.get("product")
        ).delete()
        return Response(CartSerializer(self._cart(request.user)).data)

    @action(detail=False, methods=["post"])
    def clear(self, request):
        self._cart(request.user).items.all().delete()
        return Response(CartSerializer(self._cart(request.user)).data)

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related(
            Prefetch("items")
        )

    def create(self, request):
        cart = Cart.objects.filter(user=request.user).prefetch_related("items__product").first()
        if not cart or not cart.items.exists():
            return Response({"detail": "Cart is empty"}, status=400)

        shipping_address = request.data.get("shipping_address", "")
        with transaction.atomic():
            items = list(cart.items.all())
            total = 0
            for item in items:
                total += item.product.price * item.quantity

            order = Order.objects.create(
                user=request.user,
                total_amount=total,
                shipping_address=shipping_address,
                status="CONFIRMED",
            )

            for item in items:
                stocks = list(
                    Stock.objects.select_for_update()
                    .filter(product=item.product)
                    .order_by("id")
                )
                remaining = item.quantity
                for stock in stocks:
                    available = stock.available_quantity
                    take = min(available, remaining)
                    if take:
                        stock.reserved_quantity += take
                        stock.save(update_fields=["reserved_quantity", "updated_at"])
                        OrderItem.objects.create(
                            order=order,
                            product=item.product,
                            quantity=take,
                            unit_price=item.product.price,
                        )
                        StockMovement.objects.create(
                            stock=stock,
                            movement_type="RESERVE",
                            quantity=take,
                            reference=f"ORDER-{order.id}",
                            created_by=request.user,
                        )
                        remaining -= take
                    if remaining == 0:
                        break

                if remaining:
                    raise ValueError(f"Insufficient stock for {item.product.name}")

            cart.items.all().delete()

        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"])
    def cancel(self, request, pk=None):
        with transaction.atomic():
            order = Order.objects.select_for_update().get(pk=pk, user=request.user)
            if order.status == "CANCELLED":
                return Response(OrderSerializer(order).data)
            for item in order.items.all():
                remaining = item.quantity
                stocks = list(Stock.objects.select_for_update().filter(product=item.product))
                for stock in stocks:
                    releasable = min(stock.reserved_quantity, remaining)
                    if releasable:
                        stock.reserved_quantity -= releasable
                        stock.save(update_fields=["reserved_quantity", "updated_at"])
                        StockMovement.objects.create(
                            stock=stock,
                            movement_type="RELEASE",
                            quantity=releasable,
                            reference=f"ORDER-{order.id}",
                            created_by=request.user,
                        )
                        remaining -= releasable
                    if remaining == 0:
                        break
            order.status = "CANCELLED"
            order.save(update_fields=["status", "updated_at"])
        return Response(OrderSerializer(order).data)
