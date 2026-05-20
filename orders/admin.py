from django.contrib import admin

from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("product", "price_at_purchase", "quantity")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("display_number", "user", "status", "total_price", "created_at")
    list_filter = ("status",)
    list_editable = ("status",)
    search_fields = ("user__username", "number")
    readonly_fields = ("number", "user", "total_price", "created_at")
    inlines = [OrderItemInline]

    @admin.display(description="Номер")
    def display_number(self, obj):
        return obj.display_number


admin.site.register(OrderItem)
