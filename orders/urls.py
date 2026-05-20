from django.urls import path

from .views import checkout, order_detail, orders_list

app_name = "orders"

urlpatterns = [
    path("", orders_list, name="list"),
    path("checkout/", checkout, name="checkout"),
    path("<int:pk>/", order_detail, name="detail"),
]
