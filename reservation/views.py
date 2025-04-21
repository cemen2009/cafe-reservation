from datetime import timedelta, datetime

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import QuerySet
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from reservation.forms import ReservationForm
from reservation.models import Cafe, City, Reservation, Table


class CafeListView(LoginRequiredMixin, ListView):
    model = Cafe
    template_name = "reservation/cafe_list.html"
    context_object_name = "cafes"

    def get_queryset(self) -> QuerySet:
        queryset = Cafe.objects.all()

        city_filter = self.request.GET.get("city", "all")

        if city_filter != "all":
            queryset = queryset.filter(city__id=city_filter)
        elif city_filter == "all":
            return queryset
        elif self.request.user.is_authenticated and hasattr(self.request.user, "city"):
            queryset = queryset.filter(city=self.request.user.city)

        return queryset.select_related("city")

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context["cities"] = City.objects.all().order_by("name")

        # displaying selected city in context
        selected_city = self.request.GET.get("city", "all")
        if selected_city != "all":
            context["selected_city"] = City.objects.get(id=selected_city)
        else:
            context["selected_city"] = "all"

        return context


class CafeDetailView(LoginRequiredMixin, DetailView):
    model = Cafe
    template_name = "reservation/cafe_detail.html"
    context_object_name = "cafe"


class ReservationCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Reservation
    form_class = ReservationForm
    template_name = "reservation/reservation_form.html"
    success_message = "Table booked successfully!"
    success_url = reverse_lazy("reservation:my-reservations")

    def dispatch(self, request, *args, **kwargs):
        self.table = None
        table_id = request.GET.get("table") or request.GET.get("table")

        if table_id:
            try:
                self.table = Table.objects.get(id=table_id)
            except Table.DoesNotExist:
                messages.error(request, "Selected table does not exist.")
                return redirect("reservation:cafe-list")
        else:
            messages.error(request, "No table selected.")
            return redirect("reservation:cafe-list")

        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse("reservation:my-reservations")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.localdate()

        reservation_days = [
            {
                "date": today + timedelta(days=i),
                "name": (today + timedelta(days=i)).strftime("%A"),
                "available": self.table.is_available(today + timedelta(days=i)),
            }
            for i in range(7)
        ]

        context["table"] = self.table
        context["reservation_days"] = reservation_days

        return context

    def form_valid(self, form):
        form.instance.visitor = self.request.user
        form.instance.table = self.table

        form.instance.date = self.request.POST.get("date")

        try:
            form.instance.date = datetime.strptime(form.instance.date, "%B %d, %Y").date()
        except Exception:
            messages.error(self.request, "Invalid date format.")
            return self.form_invalid(form)

        # checking range of date
        today = timezone.localdate()
        if form.instance.date < today:
            messages.error(self.request, "Reservation day cannot be earlier than today's date.")
        elif form.instance.date > today + timedelta(days=6):
            messages.error(self.request, "Reservation day cannot be later than 6 days in advance.")

        # checking is that day available
        if Reservation.objects.filter(table=self.table, date=form.instance.date).exists():
            messages.error(self.request, f"This table is already reserved for {form.instance.date}.")
            return self.form_invalid(form)

        return super().form_valid(form)

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{field}: {error}")

        print(f"FORM ERRORS: {form.errors}")
        return super().form_invalid(form)


class ReservationUpdateView(LoginRequiredMixin, UpdateView):
    model = Reservation
    form_class = ReservationForm
    template_name = "reservation/reservation_form.html"
    success_url = reverse_lazy("reservation:my-reservations")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reservation = self.get_object()
        table = reservation.table
        context["table"] = reservation.table

        today = timezone.localdate()
        reservation_days = [
            {
                "date": today + timedelta(days=i),
                "name": (today + timedelta(days=i)).strftime("%A"),
                "available": table.is_available(today + timedelta(days=i)),
            }
            for i in range(7)
        ]
        context["reservation_days"] = reservation_days

        return context

    def form_valid(self, form):
        form.instance.visitor = self.request.user
        form.instance.table = self.get_object().table
        return super().form_valid(form)


class ReservationListView(LoginRequiredMixin, ListView):
    model = Reservation
    template_name = "reservation/reservation_list.html"
    context_object_name = "reservations"

    def get_queryset(self):
        return self.request.user.reservations.filter(
            date__gte=timezone.localdate()
        ).order_by("-created_at")


class ReservationDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Reservation
    template_name = "reservation/reservation_confirm_delete.html"
    success_url = reverse_lazy("reservation:my-reservations")

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Reservation cancelled successfully.")
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        return self.request.user.reservations.all()
