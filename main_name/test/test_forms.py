from django.test import TestCase
from main_name.forms import BookingForm

class BookingFormTestCase(TestCase):
    def test_booking_form_validation(self):
        form_data = {'start_date': '2024-05-01', 'end_date': '2024-05-05'}
        form = BookingForm(data=form_data)
        self.assertTrue(form.is_valid())