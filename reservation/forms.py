from datetime import timedelta

from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone

from reservation.models import Reservation


class ReservationForm(forms.ModelForm):

    class Meta:
        model = Reservation
        fields = ["table", "date"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
        }

    def clean_date(self):
        date = self.cleaned_data.get("date")
        today = timezone.localdate()
        max_date = today + timedelta(days=2)

        if date > max_date:
            raise ValidationError("You can reserve only up 2 days in advance.")
        if date < today:
            raise ValidationError("You can't reserve for a past date.")

        return date
