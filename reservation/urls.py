from django.urls import path

from reservation.views import (
    CafeListView,
    CafeDetailView,
    ReservationCreateView,
    ReservationListView,
    ReservationUpdateView,
    ReservationDeleteView,
)

app_name = "reservation"

urlpatterns = [
    path("", CafeListView.as_view(), name="cafe-list"),
    path("cafe/<int:pk>/", CafeDetailView.as_view(), name="cafe-detail"),
    path("reserve-table/", ReservationCreateView.as_view(), name="reservation-create"),
    path("my-reservations/", ReservationListView.as_view(), name="my-reservations"),
    path("reservation-update/<int:pk>/", ReservationUpdateView.as_view(), name="reservation-update"),
    path("reservation-cancel/<int:pk>/", ReservationDeleteView.as_view(), name="reservation-cancel"),
]
