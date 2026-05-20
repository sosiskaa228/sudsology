from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import F, Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from products.models import Product

from .models import Cart, CartItem


def _cart_items_for(user):
    return (
        CartItem.objects.filter(cart__user=user)
        .select_related("product", "product__category")
        .annotate(line_total=F("quantity") * F("product__price"))
    )


def _redirect_back(request, *, default="cart:cart", default_kwargs=None):
    target = (request.POST.get("next") or "").strip()
    if target.startswith("/"):
        return redirect(target)
    return redirect(default, **(default_kwargs or {}))


@login_required
def cart_page(request):
    customer = request.user
    items = _cart_items_for(customer)
    total = items.aggregate(total=Sum("line_total")).get("total") or Decimal("0.00")
    return render(
        request,
        "cart/cart.html",
        {"customer": customer, "items": items, "total": total},
    )


@login_required
@require_POST
def cart_add(request, product_id):
    product = get_object_or_404(Product, pk=product_id, is_active=True)
    cart, _ = Cart.objects.get_or_create(user=request.user)

    item = CartItem.objects.filter(cart=cart, product=product).first()
    if item:
        item.quantity += 1
        item.save(update_fields=["quantity"])
    else:
        CartItem.objects.create(cart=cart, product=product, quantity=1)

    messages.success(request, f"«{product.name}» добавлен в корзину.")
    return _redirect_back(
        request,
        default="products:product_detail",
        default_kwargs={"pk": product.pk},
    )


@login_required
@require_POST
def cart_update(request, item_id):
    item = get_object_or_404(CartItem, pk=item_id, cart__user=request.user)
    try:
        quantity = int(request.POST.get("quantity", ""))
    except (TypeError, ValueError):
        quantity = 0

    if quantity < 1:
        messages.error(request, "Укажи количество от 1.")
        return redirect("cart:cart")

    item.quantity = quantity
    item.save(update_fields=["quantity"])
    messages.success(request, "Количество обновлено.")
    return redirect("cart:cart")


@login_required
@require_POST
def cart_remove(request, item_id):
    deleted, _ = CartItem.objects.filter(pk=item_id, cart__user=request.user).delete()
    if deleted:
        messages.success(request, "Позиция удалена из корзины.")
    else:
        messages.error(request, "Такой позиции в корзине нет.")
    return redirect("cart:cart")
