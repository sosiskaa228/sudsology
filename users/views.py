from decimal import Decimal

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.db.models import F, Sum

from cart.models import Cart, CartItem
from orders.models import Order
from .forms import ProfileUpdateForm, RegisterForm


def register(request):
    if request.user.is_authenticated:
        return redirect("users:account")

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            Cart.objects.get_or_create(user=user)
            login(request, user)
            messages.success(request, "Регистрация прошла успешно.")
            return redirect("users:account")
    else:
        form = RegisterForm()

    return render(request, "users/register.html", {"form": form})


@login_required
def account(request):
    customer = request.user
    profile_form = ProfileUpdateForm(instance=customer)

    if request.method == "POST":
        profile_form = ProfileUpdateForm(request.POST, instance=customer)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, "Профиль обновлен.")
            return redirect("users:account")
        messages.error(request, "Не удалось обновить профиль.")

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
        cart_items_count = (
            cart_items.aggregate(total=Sum("quantity")).get("total") or 0
        )
        cart_total = (
            cart_items.aggregate(total=Sum("line_total")).get("total") or Decimal("0.00")
        )
        orders = (
            Order.objects.filter(user=customer)
            .order_by("-created_at")#[:5]
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
            "profile_form": profile_form,
        },
    )
