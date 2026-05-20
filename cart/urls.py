from django.urls import path

from .views import cart_add, cart_page, cart_remove, cart_update

app_name = "cart"

urlpatterns = [
    path("", cart_page, name="cart"),
    path("add/<int:product_id>/", cart_add, name="add"),
    path("item/<int:item_id>/update/", cart_update, name="update"),
    path("item/<int:item_id>/remove/", cart_remove, name="remove"),
]
