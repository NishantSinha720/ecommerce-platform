from django.urls import path
from .views import summary, forecast

urlpatterns = [
    path("summary/", summary),
    path("forecast/", forecast),
]
