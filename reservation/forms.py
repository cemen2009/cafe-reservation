from datetime import timedelta

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
from django.db.models.functions import datetime
from django.utils import timezone

from reservation.models import City, Reservation


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


class ReservationForm(forms.ModelForm):

    class Meta:
        model = Reservation
        fields = ["table", "date"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
        }

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        time = cleaned_data.get('time')
        duration = cleaned_data.get('duration')
        table = cleaned_data.get('table')

        return cleaned_data
