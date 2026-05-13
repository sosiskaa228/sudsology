from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
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


class ProfileUpdateForm(forms.ModelForm):
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

    class Meta:
        model = get_user_model()
        fields = ("username", "email", "phone")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

    def clean_username(self):
        username = self.cleaned_data["username"].strip()
        qs = get_user_model().objects.filter(username__iexact=username).exclude(pk=self.instance.pk)
        if qs.exists():
            raise ValidationError("Пользователь с таким логином уже существует.")
        return username

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        qs = get_user_model().objects.filter(email__iexact=email).exclude(pk=self.instance.pk)
        if qs.exists():
            raise ValidationError("Пользователь с таким email уже существует.")
        return email

    def clean_phone(self):
        phone = self.cleaned_data["phone"].strip()
        if not phone:
            return phone
        qs = get_user_model().objects.filter(phone=phone).exclude(pk=self.instance.pk)
        if qs.exists():
            raise ValidationError("Пользователь с таким номером телефона уже существует.")
        return phone
