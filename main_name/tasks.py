from main_name.celery import shared_task
from django.contrib import messages
from django.utils import timezone
from .models import Booking

@shared_task
def check_overdue_bookings():
    # Query overdue bookings
    overdue_bookings = Booking.objects.filter(
        end_date__lt=timezone.now().date(),
        status='Approved'
    ).exclude(status='Returned')

    # Send alerts or notifications to users with overdue bookings
    for booking in overdue_bookings:
        user = booking.user
        message = f"Your booking for {booking.equipment.name} is overdue. Please return it as soon as possible."
        messages.error(user, message)