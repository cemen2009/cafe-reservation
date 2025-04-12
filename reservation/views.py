from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import QuerySet
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView

from reservation.forms import VisitorCreationForm
from reservation.models import Cafe, City


# class CafeListView(ListView):
#     model = Cafe
#     template_name = "reservation/cafe_list.html"
#     context_object_name = "cafes"


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


class CustomLoginView(LoginView):
    template_name = "registration/login.html"

    def get_success_url(self):
        messages.success(self.request, f"Welcome back, {self.request.user.username}!")
        return reverse_lazy("reservation:cafe-list")


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy("accounts:logout")


class SignUpView(SuccessMessageMixin, CreateView):
    form_class = VisitorCreationForm
    # do i actually need to redirect user to login after creation ?
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"
    success_message = "Congratulations, your account was created. Please login to continue."
