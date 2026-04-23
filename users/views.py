from decimal import Decimal

from django.contrib.auth import get_user_model
from django.db.models import F, Sum
from django.shortcuts import render

from cart.models import CartItem
from orders.models import Order


def account(request):
    User = get_user_model()
    customer = User.objects.filter(username="customer").first()

    cart_items = []
    cart_items_count = 0
    cart_total = Decimal("0.00")
    orders = []

    if customer:
        cart_items = (
            CartItem.objects.filter(cart__user=customer)
            .select_related("product", "cart")
            .annotate(line_total=F("quantity") * F("product__price"))
        )
        cart_items_count = cart_items.count()
        cart_total = (
            cart_items.aggregate(total=Sum("line_total")).get("total") or Decimal("0.00")
        )
        orders = (
            Order.objects.filter(user=customer)
            .order_by("-created_at")[:5]
        )

    return render(
        request,
        "users/account.html",
        {
            "customer": customer,
            "cart_items": cart_items,
            "cart_items_count": cart_items_count,
            "cart_total": cart_total,
            "orders": orders,
        },
    )
