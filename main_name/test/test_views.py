from django.test import TestCase, Client
from django.urls import reverse
from main_name.models import Equipment

class InventoryStatusReportViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.equipment = Equipment.objects.create(name='Test Equipment', availability=True)

    def test_inventory_status_report_view(self):
        response = self.client.get(reverse('inventory_report'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Equipment')