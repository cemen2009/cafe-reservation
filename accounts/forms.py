from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms

from reservation.models import City

User = get_user_model()

class VisitorCreationForm(UserCreationForm):
    city = forms.ModelChoiceField(
        queryset=City.objects.all(),
        required=False,
        empty_label="Select a city",
        label="Home city",
    )

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "city", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.city = self.cleaned_data["city"]
        if commit:
            user.save()
        return user


class VisitorUpdateForm(UserChangeForm):
        password = None

        class Meta:
            model = User
            fields = ("username", "email", "first_name", "last_name", "city")