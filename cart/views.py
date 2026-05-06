from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.db.models import F, Sum
from django.shortcuts import render

from .models import CartItem


@login_required
def cart_page(request):
    customer = request.user

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

