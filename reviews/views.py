from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST

from products.models import Product

from .forms import ReviewForm
from .models import Review
from .services import user_has_delivered_purchase


@login_required
@require_POST
def review_create(request, product_id):
    product = get_object_or_404(Product, pk=product_id, is_active=True)
    if not user_has_delivered_purchase(request.user, product):
        messages.error(
            request,
            "Отзыв можно оставить только по товару из доставленного или завершённого заказа.",
        )
        return redirect("products:product_detail", pk=product_id)
    if Review.objects.filter(user=request.user, product=product).exists():
        messages.error(request, "Ты уже оставлял отзыв на этот товар.")
        return redirect("products:product_detail", pk=product_id)

    form = ReviewForm(request.POST)
    if form.is_valid():
        try:
            Review.objects.create(
                user=request.user,
                product=product,
                rating=form.cleaned_data["rating"],
                comment=form.cleaned_data["comment"],
            )
            messages.success(request, "Отзыв сохранён.")
        except IntegrityError:
            messages.error(request, "Не удалось сохранить отзыв (дубликат).")
    else:
        messages.error(request, "Проверь оценку и текст отзыва.")

    return redirect("products:product_detail", pk=product_id)


@login_required
@require_POST
def review_delete(request, product_id):
    deleted, _ = Review.objects.filter(user=request.user, product_id=product_id).delete()
    if deleted:
        messages.success(request, "Отзыв удалён.")
    else:
        messages.error(request, "Такого отзыва нет.")
    return redirect("products:product_detail", pk=product_id)
