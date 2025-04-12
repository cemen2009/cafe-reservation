from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from reservation.models import City, Visitor


class VisitorCreationForm(UserCreationForm):
    city = forms.ModelChoiceField(
        queryset=City.objects.all(),
        required=False,
        label="Your city"
    )

    class Meta(UserCreationForm.Meta):
        model = Visitor
        fields = UserCreationForm.Meta.fields + ("email", "first_name", "last_name", "city")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        ...


class VisitorUpdateForm(UserChangeForm):
        password = None

        class Meta:
            model = Visitor
            fields = ("username", "email", "first_name", "last_name", "city")
