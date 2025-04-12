from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.shortcuts import render
from django.views.generic import ListView

from reservation.models import Cafe, City


class CafeListView(ListView):
    model = Cafe
    template_name = "reservation/cafe_list.html"
    context_object_name = "cafes"


# class CafeListView(LoginRequiredMixin, ListView):
#     model = CafeListView
#     template_name = "reservation/cafe_list.html"
#     context_object_name = "cafes"
#
#     def get_queryset(self) -> QuerySet:
#         queryset = Cafe.objects.filter(is_active=True)
#         if self.request.user.city:
#             queryset = queryset.filter(city=self.request.user.city)
#         return queryset
#
#     def get_context_data(self, *kwargs) -> dict:
#         context = super().get_context_data(**kwargs)
#         context["cities"] = City.objects.all().order_by("name")
#         return context
