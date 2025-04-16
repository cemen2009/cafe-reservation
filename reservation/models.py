import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models


class City(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Cities"
        ordering=("name",)


class Visitor(AbstractUser):
    city = models.ForeignKey(
        City,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="visitors",
        verbose_name="Home city"
    )

    def __str__(self):
        return f"{self.get_full_name() or self.username}"


class Cafe(models.Model):
    name = models.CharField(max_length=64)
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=False, related_name="cafes")
    description = models.TextField(blank=True)
    opening_hour = models.TimeField(default=datetime.time(9, 0, 0))
    closing_hour = models.TimeField(default=datetime.time(22, 0, 0))
    # rating = ...

    def available_tables_count(self) -> int:
        return self.tables.filter(is_reserved=False).count()

    def __str__(self):
        return f"{self.name} ({self.city})"

    class Meta:
        unique_together = ("name", "city")
        ordering = ("name",)


class Table(models.Model):
    number = models.IntegerField()
    seats = models.IntegerField()
    cafe = models.ForeignKey(
        Cafe,
        on_delete=models.CASCADE,
        related_name="tables"
    )
    is_reserved = models.BooleanField(default=False)

    def __str__(self):
        return f"Table #{self.number} ({self.seats})"

    class Meta:
        unique_together = ("number", "cafe")


class Reservation(models.Model):
    is_active = models.BooleanField(default=True)
    visitor = models.ForeignKey(
        Visitor,
        on_delete=models.CASCADE,
        related_name="reservations"
    )
    total_guests = models.IntegerField(
        default=1,
        help_text="Total guests amount"
    )
    table = models.ForeignKey(
        Table,
        on_delete=models.CASCADE,
        related_name="reservations"
    )
    date = models.DateField()
    time = models.TimeField()
    duration = models.IntegerField(
        help_text="Reservation duration in hours",
        verbose_name="Duration (hours)"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Reservation #{self.id} - {self.visitor} at table {self.table.number}"

    class Meta:
        ordering = ("-created_at",)
