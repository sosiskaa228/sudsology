from django.urls import path

from .views import cart_page

app_name = "cart"

urlpatterns = [
    path("", cart_page, name="cart"),
]

