from rest_framework.routers import DefaultRouter
from .views import WarehouseViewSet, StockViewSet, StockMovementViewSet

router = DefaultRouter()
router.register("warehouses", WarehouseViewSet)
router.register("stock", StockViewSet)
router.register("stock-movements", StockMovementViewSet)

urlpatterns = router.urls
