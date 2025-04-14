from django.urls import path

from reservation.views import CafeListView

app_name = "reservation"

urlpatterns = [
    path("", CafeListView.as_view(), name="cafe-list"),
]
