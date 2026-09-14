from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import TokenRefreshView
from users.views import RegisterView
from products.views import CategoryViewSet

urlpatterns = [
    path("admin/", admin.site.urls),

    # Authentication
    path("api/auth/register/", RegisterView.as_view()),
    path(
        "api/auth/login/",
        __import__(
            "rest_framework_simplejwt.views",
            fromlist=["TokenObtainPairView"]
        ).TokenObtainPairView.as_view()
    ),
    path("api/auth/refresh/", TokenRefreshView.as_view()),

    # Products
    path("api/products/", include("products.urls")),

    # Direct category endpoint
    path(
        "api/categories/",
        CategoryViewSet.as_view({
            "get": "list",
            "post": "create"
        })
    ),

    # Other APIs
    path("api/inventory/", include("inventory.urls")),
    path("api/orders/", include("orders.urls")),
    path("api/analytics/", include("analytics.urls")),
]