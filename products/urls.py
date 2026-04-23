from django.urls import path

from . import views

app_name = "products"

urlpatterns = [
    path("", views.home, name="home"),
    path("catalog/", views.ProductListView.as_view(), name="catalog"),
    path("product/<int:pk>/", views.ProductDetailView.as_view(), name="product_detail"),
]

