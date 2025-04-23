from django.contrib import admin

from reservation.models import Visitor, Reservation, City, Cafe, Table


class TableAdmin(admin.ModelAdmin):
    list_display = ("number", "cafe", "seats")
    list_filter = ("cafe",)
    search_fields = ("number", "cafe__name")
    ordering = ("cafe", "seats")


class VisitorAdmin(admin.ModelAdmin):
    list_display = ("username", "get_full_name", "city__name")
    ordering = ("city__name", "first_name")


admin.site.register(Visitor, VisitorAdmin)
admin.site.register(Table, TableAdmin)
admin.site.register(Cafe)
admin.site.register(City)
admin.site.register(Reservation)
