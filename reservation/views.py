from datetime import timedelta

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import QuerySet
from django.urls import reverse
from django.utils import timezone
from django.views.generic import ListView, CreateView, DetailView

from reservation.forms import ReservationForm
from reservation.models import Cafe, City, Reservation, Table


class CafeListView(LoginRequiredMixin, ListView):
    model = Cafe
    template_name = "reservation/cafe_list.html"
    context_object_name = "cafes"

    def get_queryset(self) -> QuerySet:
        queryset = Cafe.objects.all()

        city_filter = self.request.GET.get("city")

        if city_filter and city_filter != "all":
            queryset = queryset.filter(city__id=city_filter)
        elif self.request.user.is_authenticated and hasattr(self.request.user, "city") and self.request.user.city:
            queryset = queryset.filter(city=self.request.user.city)

        return queryset.select_related("city").prefetch_related("tables")
        # return queryset

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context["cities"] = City.objects.all().order_by("name")
        return context


class CafeDetailView(LoginRequiredMixin, DetailView):
    model = Cafe
    template_name = "reservation/cafe_detail.html"
    context_object_name = "cafe"


# class ReservationCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
#     model = Reservation
#     form_class = ReservationForm
#     template_name = "reservation/reservation_create.html"
#     success_message = "Table booked successfully!"
#
#     def get_success_url(self):
#         return reverse_lazy("reservation:my-reservations")  # TODO: add my-reservations to urls.py
#
#     def form_valid(self, form):
#         form.instance.visitor = self.request.user
#         return super().form_valid(form)
#
#     def get_form_kwargs(self):
#         kwargs = super().get_form_kwargs()
#         kwargs["initial"] = {"table": self.kwargs.get("table_id")}
#         return kwargs


# class ReservationCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
#     model = Reservation
#     form_class = ReservationForm
#     template_name = "reservation/reservation_create.html"
#     success_message = "Table booked successfully!"
#
#     def get_success_url(self):
#         return reverse_lazy("reservation:my-reservations")
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         table_id = self.request.GET.get('table')
#         if table_id:
#             try:
#                 context['table'] = Table.objects.get(id=table_id)
#             except Table.DoesNotExist:
#                 pass
#         return context
#
#     def form_valid(self, form):
#         form.instance.visitor = self.request.user
#         table_id = self.request.GET.get('table')
#         if table_id:
#             try:
#                 form.instance.table = Table.objects.get(id=table_id)
#             except Table.DoesNotExist:
#                 pass
#         return super().form_valid(form)


class ReservationCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Reservation
    form_class = ReservationForm
    template_name = "reservation/reservation_create.html"
    success_message = "Table booked successfully!"

    def get_success_url(self):
        return reverse("reservation:my-reservations")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        table_id = self.request.GET.get("table")
        context["table"] = Table.objects.get(id=table_id)

        # adding dates to the template
        today = timezone.localdate()
        context.update({
            "today": today,
            "tomorrow": today + timedelta(days=1),
            "day after tomorrow": today + timedelta(days=2),
        })

        return context

    def get_available_slots(self, table_id, date):
        """Calculate available time slots for the given table and date"""
        # Implement your slot calculation logic here
        # Example: return ['10:00', '11:00', '12:00']
        return []

    def get_initial(self):
        initial = super().get_initial()
        table_id = self.request.GET.get('table')
        if table_id:
            initial['table'] = table_id
        if 'date' in self.request.GET:
            initial['date'] = self.request.GET['date']
        return initial

    def form_valid(self, form):
        form.instance.visitor = self.request.user
        table_id = self.request.GET.get('table')

        if not table_id:
            messages.error(self.request, "No table selected")
            return self.form_invalid(form)

        try:
            table = Table.objects.get(id=table_id)

            form.instance.table = table
            response = super().form_valid(form)
            messages.success(self.request, self.success_message)
            return response

        except Table.DoesNotExist:
            messages.error(self.request, "Selected table does not exist")
            return self.form_invalid(form)

    def form_invalid(self, form):
        """Add form errors to messages"""
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{field}: {error}")
        return super().form_invalid(form)


class ReservationListView(LoginRequiredMixin, ListView):
    model = Reservation
    template_name = "reservation/my_reservations_list.html"
    context_object_name = "reservations"

    def get_queryset(self):
        return self.request.user.reservations.filter(
            date__gte=timezone.localdate()
        ).order_by("-created_at")
