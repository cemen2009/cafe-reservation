from django import forms

from reservation.models import Reservation


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
