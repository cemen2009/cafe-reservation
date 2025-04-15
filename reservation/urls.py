from django.urls import path

from reservation.views import (
    CafeListView,
    CafeDetailView,
    ReservationCreateView,
)

app_name = "reservation"

urlpatterns = [
    path("", CafeListView.as_view(), name="cafe-list"),
    path("cafe/<int:pk>/", CafeDetailView.as_view(), name="cafe-detail"),
    # path("reserve-table/<int:pk>/", ReservationCreateView.as_view(), name="reservation-create"),
    path("reserve-table/", ReservationCreateView.as_view(), name="reservation-create"),
    path("reservations/", ReservationCreateView.as_view(), name="my-reservations"),
]
