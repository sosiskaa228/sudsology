from django.contrib.auth import get_user_model
from django.shortcuts import render

from .models import Order


def orders_list(request):
    User = get_user_model()
    customer = User.objects.filter(username="customer").first()

    orders = []
    if customer:
        orders = Order.objects.filter(user=customer).order_by("-created_at")

    return render(request, "orders/orders_list.html", {"customer": customer, "orders": orders})

from django.shortcuts import render
