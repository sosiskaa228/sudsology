from django import forms

from .models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ("rating", "comment")
        widgets = {
            "rating": forms.Select(
                choices=[(i, f"{i} из 5") for i in range(1, 6)],
                attrs={"class": "form-select form-select-sm"},
            ),
            "comment": forms.Textarea(
                attrs={
                    "class": "form-control form-control-sm",
                    "rows": 3,
                    "placeholder": "Коротко о товаре",
                },
            ),
        }
