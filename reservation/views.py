from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import QuerySet
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView

from reservation.forms import VisitorCreationForm, VisitorUpdateForm, ReservationForm
from reservation.models import Cafe, City, Visitor, Reservation


class CafeListView(LoginRequiredMixin, ListView):
    model = Cafe
    template_name = "reservation/cafe_list.html"
    context_object_name = "cafes"

    def get_queryset(self) -> QuerySet:
        queryset = Cafe.objects.all()
        if self.request.user.city:
            queryset = queryset.filter(city=self.request.user.city)
        return queryset

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context["cities"] = City.objects.all().order_by("name")
        return context


class CafeDetailView(LoginRequiredMixin, DetailView):
    model = Cafe
    template_name = "reservation/cafe_detail.html"
    context_object_name = "cafe"


class ReservationCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Reservation
    form_class = ReservationForm
    template_name = "reservation/reservation_create.html"
    success_message = "Table booked successfully!"

    def get_success_url(self):
        return reverse_lazy("reservation:my-reservations")  # TODO: add my-reservations to urls.py

    def form_valid(self, form):
        form.instance.visitor = self.request.user
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["initial"] = {"table": self.kwargs.get("table_id")}
        return kwargs


class MyReservationsListView(LoginRequiredMixin, ListView):
    model = Reservation
    template_name = "reservation/my_reservations_list.html"
    context_object_name = "reservations"

    def get_queryset(self):
        return self.request.user.reservations.filter(is_active=True).order_by("-created_at")


# accounts
# TODO: refactor after implementing MVP
class CustomLoginView(LoginView):
    template_name = "registration/login.html"

    def get_success_url(self):
        messages.success(self.request, f"Welcome back, {self.request.user.username}!")
        return reverse_lazy("reservation:cafe-list")


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy("logout")
    template_name = "registration/logout.html"


class SignUpView(SuccessMessageMixin, CreateView):
    form_class = VisitorCreationForm
    # do i actually need to redirect user to login after creation ?
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"
    success_message = "Congratulations, your account was created. Please login to continue."


class VisitorUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Visitor
    form_class = VisitorUpdateForm
    template_name = "registration/profile.html"
    success_url = reverse_lazy("reservation:profile")
    success_message = "Your profile was updated successfully!"

    def get_object(self):
        return self.request.user
