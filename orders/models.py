from django.db import models
from django.conf import settings

from products.models import Product


class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Ожидает"
        PAID = "paid", "Оплачен"
        SHIPPED = "shipped", "Отправлен"
        COMPLETED = "completed", "Завершён"
        CANCELLED = "cancelled", "Отменён"

    number = models.PositiveIntegerField(unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Заказ"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"Заказ {self.display_number}"

    @property
    def display_number(self) -> str:
        return f"{self.number:04d}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price_at_purchase = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()

    class Meta:
        verbose_name = "Позиция заказа"

    def __str__(self) -> str:
        return f"{self.product_id} x{self.quantity}"

    @property
    def line_total(self):
        return self.price_at_purchase * self.quantity
