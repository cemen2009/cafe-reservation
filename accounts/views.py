from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from accounts.forms import VisitorCreationForm, VisitorUpdateForm
from reservation.models import Visitor


class CustomLoginView(LoginView):
    template_name = "registration/login.html"

    def get_success_url(self):
        messages.success(self.request, f"Welcome back, {self.request.user.username}!")
        return reverse_lazy("reservation:cafe-list")


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy("accounts:logout")
    template_name = "registration/logout.html"


class SignUpView(SuccessMessageMixin, CreateView):
    form_class = VisitorCreationForm
    # do i actually need to redirect user to login after creation ?
    success_url = reverse_lazy("accounts:login")
    template_name = "registration/signup.html"
    success_message = "Congratulations, your account was created. Please login to continue."


class VisitorUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Visitor
    form_class = VisitorUpdateForm
    template_name = "registration/profile.html"
    success_url = reverse_lazy("reservation:cafe-list")
    success_message = "Your profile was updated successfully!"

    def get_object(self):
        return self.request.user
