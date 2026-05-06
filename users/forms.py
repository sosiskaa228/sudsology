from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator


class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label="Email",
        error_messages={
            "required": "Введите email.",
            "invalid": "Введите email в формате name@example.com.",
        },
    )
    phone = forms.CharField(
        required=False,
        label="Телефон",
        validators=[
            RegexValidator(
                regex=r"^\+?\d{10,15}$",
                message="Телефон должен содержать 10-15 цифр (+ в начале).",
            )
        ],
    )

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ("username", "email", "phone")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"
