from django.shortcuts import render
from django.views.generic import DetailView, ListView

from .models import Product
from reviews.models import Review


def home(request):
    return render(request, "home.html")


class ProductListView(ListView):
    model = Product
    template_name = "products/product_list.html"


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
