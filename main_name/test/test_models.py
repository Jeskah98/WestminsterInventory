from django.test import TestCase
from main_name.models import Equipment, Booking

class EquipmentModelTestCase(TestCase):
    def test_equipment_creation(self):
        equipment = Equipment.objects.create(name='Test Equipment', availability=True)
        self.assertEqual(Equipment.objects.count(), 1)
        self.assertEqual(equipment.name, 'Test Equipment')

class BookingModelTestCase(TestCase):
    def test_booking_creation(self):
        equipment = Equipment.objects.create(name='Test Equipment', availability=True)
        booking = Booking.objects.create(equipment=equipment, start_date='2024-05-01', end_date='2024-05-05')
        self.assertEqual(Booking.objects.count(), 1)
        self.assertEqual(booking.equipment, equipment)
