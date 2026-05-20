from django.db.models.functions import Lower
from django.shortcuts import render
from django.views.generic import DetailView, ListView

from .models import Product
from reviews.forms import ReviewForm
from reviews.models import Review
from reviews.services import user_has_delivered_purchase


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
        context["current_q"] = (get.get("q") or "").strip()
        context["current_sort"] = get.get("sort") or "new"
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = "products/product_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.object
        user = self.request.user
        context["reviews"] = (
             Review.objects.filter(product=product)
            .select_related("user")
            .order_by("-created_at")
        )
        context["review_form"] = None
        context["own_review"] = None
        context["can_leave_review"] = False
        if user.is_authenticated:
            context["own_review"] = Review.objects.filter(user=user, product=product).first()
            context["can_leave_review"] = (
                user_has_delivered_purchase(user, product)
                and context["own_review"] is None
            )
            if context["can_leave_review"]:
                context["review_form"] = ReviewForm()
        return context
