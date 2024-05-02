from django.test import TestCase, Client
from main_name.models import Equipment

class IntegrationTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.equipment = Equipment.objects.create(name='Test Equipment', availability=True)

    def test_booking_integration(self):
        response = self.client.post('/make_booking/', {'equipment': self.equipment.id, 'start_date': '2024-05-01', 'end_date': '2024-05-05'})
        self.assertEqual(response.status_code, 302)