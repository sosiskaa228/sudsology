from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Order


@login_required
def orders_list(request):
    customer = request.user

    orders = []
    if customer:
        orders = Order.objects.filter(user=customer).order_by("-created_at")

    return render(request, "orders/orders_list.html", {"customer": customer, "orders": orders})
