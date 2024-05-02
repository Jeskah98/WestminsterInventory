from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Booking, User, Equipment
from .forms import CustomUserCreationForm,EquipmentForm
from functools import wraps
from django.http import HttpResponseForbidden
from datetime import date
from django.utils import timezone
import datetime

def staff_member_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_staff:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("You are not authorized to access this page.")
    return _wrapped_view

@login_required
@staff_member_required
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html',)

def pending_booking(request):
    pending_bookings = Booking.objects.filter(status='pending')
    return render(request, 'pending_booking.html', {'pending_bookings': pending_bookings})

@login_required
@staff_member_required
def approve_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    booking.status = 'approved'
    booking.save()
    return redirect('admin_dashboard')

@login_required
@staff_member_required
def reject_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    booking.status = 'rejected'
    booking.save()
    return redirect('admin_dashboard')

@login_required
@staff_member_required
def pending_registrations(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        action = request.POST.get('action')
        if action == 'approve':
            user = User.objects.get(id=user_id)
            user.is_active = True
            user.save()
        elif action == 'reject':
            user = User.objects.get(id=user_id)
            user.delete()
    pending_users = User.objects.filter(is_active=False)
    return render(request, 'pending_registrations.html', {'pending_users': pending_users})

@login_required
@staff_member_required
def approve_registration(request, user_id):
    user = User.objects.get(id=user_id)
    user.is_active = True
    user.save()
    return redirect('pending_registrations')

@login_required
@staff_member_required
def reject_registration(request, user_id):
    user = User.objects.get(id=user_id)
    user.delete()
    return redirect('pending_registrations')

def equipment_list(request):
    total_count = Equipment.objects.count()
    available_count = Equipment.objects.filter(availability=True).count()
    on_site_count = Equipment.objects.filter(on_site_only=True).count()
    
    today = datetime.date.today()
    booked_count = Booking.objects.filter(start_date__lte=today, end_date__gte=today).count()

    equipments = Equipment.objects.all()
    return render(request, 'equipment_list.html', {
        'equipments': equipments,
        'total_count': total_count,
        'available_count': available_count,
        'on_site_count': on_site_count,
        'booked_count': booked_count,
    })

def add_equipment(request):
    if request.method == 'POST':
        form = EquipmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('equipment_list')
    else:
        form = EquipmentForm()
    return render(request, 'add_equipment.html', {'form': form})

def edit_equipment(request, equipment_id):
    equipment = get_object_or_404(Equipment, pk=equipment_id)
    if request.method == 'POST':
        form = EquipmentForm(request.POST, instance=equipment)
        if form.is_valid():
            form.save()
            return redirect('equipment_list')
    else:
        form = EquipmentForm(instance=equipment)
    return render(request, 'edit_equipment.html', {'form': form})

def delete_equipment(request, equipment_id):
    equipment = get_object_or_404(Equipment, pk=equipment_id)
    equipment.delete()
    return redirect('equipment_list')

def list_users(request):
    users = User.objects.all()  # Query all users
    return render(request, 'user_list.html', {'users': users})

def update_user_role(request, user_id):
    if request.method == 'POST':
        new_role = request.POST.get('new_role')
        user = User.objects.get(pk=user_id)
        user.role = new_role
        user.save()
        return redirect('user_list')
    else:
        # Render a form to update user role
        user = User.objects.get(pk=user_id)
        return render(request, 'update_user_role.html', {'user': user})
    
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return redirect('user_list')

def add_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'add_user.html', {'form': form})

def inventory_status_report(request):
    overdue_bookings = Booking.objects.filter(
        end_date__lt=timezone.now().date(),
        status='approved',
        returned=False
    )
    return render(request, 'inventory_report.html', {'overdue_bookings': overdue_bookings})


def equipment_usage_history(request):
    bookings = Booking.objects.all()
    return render(request, 'equipment_report.html', {'bookings': bookings})