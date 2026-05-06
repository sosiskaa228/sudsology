from decimal import Decimal

from django.contrib import messages
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.db.models import F, Sum

from cart.models import CartItem
from orders.models import Order
from .forms import CustomPasswordChangeForm, ProfileUpdateForm, RegisterForm


def register(request):
    if request.user.is_authenticated:
        return redirect("users:account")

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
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
    password_form = CustomPasswordChangeForm(user=customer)

    if request.method == "POST":
        form_type = request.POST.get("form_type")
        if form_type == "profile":
            profile_form = ProfileUpdateForm(request.POST, instance=customer)
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, "Профиль обновлен.")
                return redirect("users:account")
            messages.error(request, "Не удалось обновить профиль. Проверь поля.")
        elif form_type == "password":
            password_form = CustomPasswordChangeForm(customer, request.POST)
            if password_form.is_valid():
                updated_user = password_form.save()
                update_session_auth_hash(request, updated_user)
                messages.success(request, "Пароль успешно изменен.")
                return redirect("users:account")
            messages.error(request, "Не удалось изменить пароль. Проверь введенные данные.")

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
            "profile_form": profile_form,
            "password_form": password_form,
        },
    )
