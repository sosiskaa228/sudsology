from decimal import Decimal

from django.contrib.auth import get_user_model
from django.db.models import F, Sum
from django.shortcuts import render

from .models import CartItem


def cart_page(request):
    User = get_user_model()
    customer = User.objects.filter(username="customer").first()

    items = []
    total = Decimal("0.00")
    if customer:
        items = (
            CartItem.objects.filter(cart__user=customer)
            .select_related("product")
            .annotate(line_total=F("quantity") * F("product__price"))
        )
        total = items.aggregate(total=Sum("line_total")).get("total") or Decimal("0.00")

    return render(request, "cart/cart.html", {"customer": customer, "items": items, "total": total})

from django.shortcuts import render

