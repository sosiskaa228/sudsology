from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Max
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from cart.models import CartItem

from .models import Order, OrderItem


def _next_order_number() -> int:
    last = Order.objects.aggregate(m=Max("number"))["m"]
    return (last or 0) + 1


@login_required
def orders_list(request):
    customer = request.user
    orders = Order.objects.filter(user=customer).order_by("-created_at")
    return render(
        request,
        "orders/orders_list.html",
        {"customer": customer, "orders": orders},
    )


@login_required
def order_detail(request, pk):
    order = get_object_or_404(
        Order.objects.prefetch_related("items__product"),
        pk=pk,
        user=request.user,
    )
    return render(
        request,
        "orders/order_detail.html",
        {"customer": request.user, "order": order},
    )


@login_required
@require_POST
def checkout(request):
    customer = request.user
    items = list(
        CartItem.objects.filter(cart__user=customer).select_related("product")
    )

    if not items:
        messages.error(request, "Корзина пустая — нечего оформлять.")
        return redirect("cart:cart")

    total = sum(
        (item.product.price * item.quantity for item in items),
        Decimal("0.00"),
    )

    with transaction.atomic():
        order = Order.objects.create(
            number=_next_order_number(),
            user=customer,
            total_price=total,
            status=Order.Status.PENDING,
        )
        for item in items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                price_at_purchase=item.product.price,
                quantity=item.quantity,
            )

        CartItem.objects.filter(cart__user=customer).delete()

    messages.success(request, f"Заказ №{order.display_number} оформлен.")
    return redirect("orders:detail", pk=order.pk)
