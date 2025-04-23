from datetime import timedelta
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model

from reservation.models import City, Cafe, Table, Reservation

User = get_user_model()


class ModelTests(TestCase):

    def setUp(self):
        self.city = City.objects.create(name="Lviv")
        self.visitor = User.objects.create_user(username="john", password="password123", city=self.city)
        self.cafe = Cafe.objects.create(name="Test Cafe", city=self.city)
        self.table = Table.objects.create(number=1, seats=4, cafe=self.cafe)
        self.date = timezone.localdate()
        self.reservation = Reservation.objects.create(visitor=self.visitor, table=self.table, date=self.date)

    def test_city_str(self):
        self.assertEqual(str(self.city), "Lviv")

    def test_visitor_str(self):
        self.assertEqual(str(self.visitor), "john")

    def test_cafe_str(self):
        self.assertEqual(str(self.cafe), "Test Cafe (Lviv)")

    def test_table_str(self):
        self.assertEqual(str(self.table), "Table #1 (4)")

    def test_table_is_available_false(self):
        self.assertFalse(self.table.is_available(self.date))

    def test_table_is_available_true(self):
        tomorrow = self.date + timedelta(days=1)
        self.assertTrue(self.table.is_available(tomorrow))

    def test_cafe_available_tables_today_count(self):
        self.assertEqual(self.cafe.available_tables_today_count(), 0)

    def test_reservation_str(self):
        self.assertIn("Reservation #", str(self.reservation))

    def test_reservation_is_active(self):
        self.assertTrue(self.reservation.is_active())


class ViewTests(TestCase):

    def setUp(self):
        self.city = City.objects.create(name="Kyiv")
        self.visitor = User.objects.create_user(username="anna", password="testpass", city=self.city)
        self.client.login(username="anna", password="testpass")

        self.cafe = Cafe.objects.create(name="Green Cafe", city=self.city)
        self.table = Table.objects.create(number=2, seats=2, cafe=self.cafe)
        self.today = timezone.localdate()

    def test_create_reservation_view(self):
        url = reverse("reservation:reservation-create") + f"?table={self.table.id}"
        response = self.client.post(url, data={
            "date": (self.today + timedelta(days=1)).strftime("%B %d, %Y"),
            "special_requests": "Window seat if possible",
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Reservation.objects.count(), 1)

    def test_reservation_update_view(self):
        reservation = Reservation.objects.create(visitor=self.visitor, table=self.table, date=self.today)
        url = reverse("reservation:reservation-update", args=[reservation.id])
        response = self.client.post(url, data={
            "date": (self.today + timedelta(days=1)).strftime("%Y-%m-%d"),
            "table": self.table.id,
        })
        self.assertEqual(response.status_code, 302)

    def test_reservation_delete_view(self):
        reservation = Reservation.objects.create(visitor=self.visitor, table=self.table, date=self.today)
        url = reverse("reservation:reservation-cancel", args=[reservation.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Reservation.objects.filter(id=reservation.id).exists())
