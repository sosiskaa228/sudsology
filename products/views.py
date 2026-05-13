from django.db.models.functions import Lower
from django.shortcuts import render
from django.views.generic import DetailView, ListView

from .models import Category, Product
from reviews.models import Review


def home(request):
    return render(request, "home.html")


class ProductListView(ListView):
    model = Product
    template_name = "products/product_list.html"
    context_object_name = "products"

    def get_queryset(self):
        get = self.request.GET
        qs = Product.objects.filter(is_active=True).select_related("category")

        text = (get.get("q") or "").strip()
        if text:
            qs = qs.annotate(_qname=Lower("name")).filter(
                _qname__contains=text.lower(),
            )

        cat = get.get("category") or ""
        if cat.isdigit():
            qs = qs.filter(category_id=int(cat))

        how = get.get("sort") or "new"
        if how == "cheap":
            qs = qs.order_by("price")
        elif how == "expensive":
            qs = qs.order_by("-price")
        elif how == "name":
            qs = qs.order_by("name")
        else:
            qs = qs.order_by("-created_at")

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        get = self.request.GET
        cat_raw = get.get("category") or ""
        context["categories"] = Category.objects.order_by("name")
        context["current_q"] = (get.get("q") or "").strip()
        context["category_id"] = int(cat_raw) if cat_raw.isdigit() else None
        context["current_sort"] = get.get("sort") or "new"
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = "products/product_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["reviews"] = (
            Review.objects.filter(product=self.object)
            .select_related("user")
            .order_by("-created_at")
        )
        return context
