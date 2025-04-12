from django.contrib import admin

from reservation.models import Visitor, Reservation, City, Cafe, Table


class TableAdmin(admin.ModelAdmin):
    list_display = ("number", "cafe", "seats", "is_reserved")
    list_filter = ("cafe",)
    search_fields = ("number", "cafe__name")
    ordering = ("cafe", "seats")


admin.site.register(Visitor)
admin.site.register(Table, TableAdmin)
admin.site.register(Cafe)
admin.site.register(City)
admin.site.register(Reservation)
