from __future__ import annotations

from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from cart.models import Cart, CartItem
from orders.models import Order, OrderItem
from products.models import Category, Product
from reviews.models import Review


class Command(BaseCommand):
    help = "Seed demo data for Sudsology (idempotent)."

    def handle(self, *args, **options):
        User = get_user_model()

        customer, _ = User.objects.get_or_create(
            username="customer",
            defaults={"email": "customer@example.com"},
        )
        customer.set_password("Customer12345!")
        customer.save()

        soap, _ = Category.objects.get_or_create(name="Мыло", parent=None)
        bath, _ = Category.objects.get_or_create(name="Ванна", parent=None)
        care, _ = Category.objects.get_or_create(name="Уход", parent=None)

        p1, _ = Product.objects.get_or_create(
            name="Мыло “Мята и лайм”",
            defaults={
                "description": "Свежий аромат мяты и лайма. Мягкое очищение для ежедневного ухода.",
                "price": Decimal("12.90"),
                "stock_quantity": 25,
                "category": soap,
                "is_active": True,
            },
        )
        p2, _ = Product.objects.get_or_create(
            name="Бомбочка “Лаванда”",
            defaults={
                "description": "Расслабляющая бомбочка для ванны с лёгким ароматом лаванды.",
                "price": Decimal("8.50"),
                "stock_quantity": 60,
                "category": bath,
                "is_active": True,
            },
        )
        p3, _ = Product.objects.get_or_create(
            name="Скраб “Кокос”",
            defaults={
                "description": "Сахарный скраб с кокосовым маслом. Нежно обновляет кожу.",
                "price": Decimal("16.00"),
                "stock_quantity": 40,
                "category": care,
                "is_active": True,
            },
        )

        Review.objects.get_or_create(
            user=customer,
            product=p1,
            defaults={"rating": 5, "comment": "Очень приятный аромат, кожу не сушит. Возьму ещё."},
        )
        Review.objects.get_or_create(
            user=customer,
            product=p2,
            defaults={"rating": 4, "comment": "Классная, но хотелось бы чуть сильнее аромат."},
        )

        cart, _ = Cart.objects.get_or_create(user=customer)
        CartItem.objects.update_or_create(cart=cart, product=p1, defaults={"quantity": 1})
        CartItem.objects.update_or_create(cart=cart, product=p2, defaults={"quantity": 2})

        order, _ = Order.objects.get_or_create(
            user=customer,
            status=Order.Status.PAID,
            defaults={"total_price": Decimal("29.90")},
        )
        OrderItem.objects.update_or_create(
            order=order,
            product=p1,
            defaults={"price_at_purchase": p1.price, "quantity": 1},
        )
        OrderItem.objects.update_or_create(
            order=order,
            product=p2,
            defaults={"price_at_purchase": p2.price, "quantity": 2},
        )

        self.stdout.write(self.style.SUCCESS("Demo data created/updated."))

