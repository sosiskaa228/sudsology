from orders.models import Order, OrderItem

_REVIEW_OK_STATUSES = (Order.Status.SHIPPED, Order.Status.COMPLETED)


def user_has_delivered_purchase(user, product) -> bool:
    if not user.is_authenticated:
        return False
    return OrderItem.objects.filter(
        product_id=product.pk,
        order__user=user,
        order__status__in=_REVIEW_OK_STATUSES,
    ).exists()
