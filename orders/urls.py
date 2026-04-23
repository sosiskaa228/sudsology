from django.urls import path

from .views import orders_list

app_name = "orders"

urlpatterns = [
    path("", orders_list, name="list"),
]

