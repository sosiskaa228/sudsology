from django.views.generic import ListView

from .models import Review


class ReviewListView(ListView):
    model = Review
    template_name = "reviews/reviews.html"

    def get_queryset(self):
        return (
            Review.objects.select_related("user", "product")
            .order_by("-created_at")
        )
