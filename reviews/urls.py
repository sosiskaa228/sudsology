from django.urls import path

from . import views

app_name = "reviews"

urlpatterns = [
    path("", views.ReviewListView.as_view(), name="list"),
    path("product/<int:product_id>/add/", views.review_create, name="create"),
    path("product/<int:product_id>/delete/", views.review_delete, name="delete"),
]

