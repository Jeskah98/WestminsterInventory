from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .forms import CustomAuthenticationForm, CustomUserCreationForm, BookingForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .models import Equipment, Booking, User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from datetime import date

def home(request):
    return render(request, 'home.html')

def user_register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            role = form.cleaned_data['role']
            
            # Create user with pending status
            user = User.objects.create_user(username=username, password=password)
            user.is_active = False  # Deactivate until admin approval
            user.role = role
            user.save()
            return redirect('registration_success')
    else:
        form = CustomUserCreationForm()
    return render(request, 'user_register.html', {'form': form})

def registration_success(request):
    return render(request, 'registration_success.html')

def user_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None and user.is_active:
                login(request, user)
                if user.role == 'staff':
                    return redirect('admin_dashboard')  # Redirect staff (admin) users to admin dashboard
                else:
                    return redirect('user_dashboard')  # Redirect student users to user dashboard
        else:
                form.add_error(None, 'Invalid username or password/ Please check your account is active')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'user_login.html', {'form': form})

@login_required
def user_dashboard(request):
    reservations = Booking.objects.filter(user=request.user, status='reserved')
    booked_equipment_ids = reservations.values_list('equipment_id', flat=True)
    pending_bookings = Booking.objects.filter(user=request.user, status='pending')
    current_bookings = Booking.objects.filter(user=request.user, status='approved', end_date__gte=date.today(), returned=False)
    rejected_bookings = Booking.objects.filter(user=request.user, status='rejected')
    past_bookings = Booking.objects.filter(user=request.user, status='approved', returned=True)

    context = {
        'booked_equipment_ids': booked_equipment_ids,
        'reservations': reservations,
        'pending_bookings': pending_bookings,
        'current_bookings': current_bookings,
        'rejected_bookings': rejected_bookings,
        'past_bookings': past_bookings,
    }
    return render(request, 'user_dashboard.html', context)

@login_required
def view_equipment(request):
    equipments = Equipment.objects.all()
    # Handle filtering based on return date
    return_date_filter = request.GET.get('return_date')
    if return_date_filter:
        equipments = equipments.filter(return_date=return_date_filter)

    # Handle filtering based on equipment type
    equipment_type_filter = request.GET.get('equipment_type')
    if equipment_type_filter:
        equipments = equipments.filter(type=equipment_type_filter)

    # Handle sorting
    sort_by = request.GET.get('sort_by')
    if sort_by:
        equipments = equipments.order_by(sort_by)

    return render(request, 'view_equipment.html', {'equipments': equipments})

@login_required
def search_equipment(request):
    query = request.GET.get('q')
    equipments = Equipment.objects.all()
    if query:
        equipments = equipments.filter(
        Q(id__icontains=query) |   # Search by ID
        Q(asset_tag__icontains=query) |   # Search by asset tag
        Q(name__icontains=query) |   # Search by name
        Q(type__icontains=query)   # Search by type
    )
    return render(request, 'search_equipment.html', {'equipments': equipments, 'query': query})


@login_required
def make_booking(request, equipment_id):
    equipment = get_object_or_404(Equipment, id=equipment_id)

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            if not equipment.availability:
                messages.error(request, f"{equipment.name} is not available for booking.")
                return redirect('equipment_list')  # Redirect to equipment list page or another appropriate page

            booking = form.save(commit=False)
            booking.equipment = equipment
            booking.user = request.user
            booking.status = 'pending'  # Set status to pending for admin approval
            booking.save()

            # Decrement equipment quantity by 1
            equipment.quantity -= 1
            if equipment.quantity <= 0:
                equipment.availability = False
            equipment.save()
            return redirect('booking_confirmation')
    else:
        initial_data = {'user': request.user, 'equipment': equipment}
        form = BookingForm(initial=initial_data)
    return render(request, 'make_booking.html', {'form': form, 'equipment': equipment})

@login_required
def booking_confirmation(request):
    return render(request, 'booking_confirmation.html')

@login_required
def view_bookings(request):
    pending_bookings = Booking.objects.filter(status='pending')
    return render(request, 'view_bookings.html', {'pending_bookings': pending_bookings})


@login_required
def return_booking(request, booking_id):
    booking = Booking.objects.get(id=booking_id)
    # Increment quantity of equipment item
    booking.equipment.quantity += 1
    booking.equipment.save()
    # Update booking status to "Returned"
    booking.returned = True
    booking.save()
    return redirect('user_dashboard')

def book_from_past_booking(request, booking_id):
    past_booking = get_object_or_404(Booking, id=booking_id)
    
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            equipment = past_booking.equipment

            if not equipment.availability:
                messages.error(request, f"{equipment.name} is not available for booking.")
                return redirect('equipment_list')  # Redirect to equipment list page or another appropriate page

            booking = form.save(commit=False)
            booking.equipment = equipment
            booking.user = request.user
            booking.status = 'pending'  # Set status to pending for admin approval
            booking.save()

            # Decrement equipment quantity by 1
            equipment.quantity -= 1
            if equipment.quantity <= 0:
                equipment.availability = False
            equipment.save()

            return redirect('booking_confirmation')
    else:
        initial_data = {
            'equipment': past_booking.equipment,
            'start_date': past_booking.start_date,
            'end_date': past_booking.end_date,
        }
        form = BookingForm(initial=initial_data)
    
    return render(request, 'book_from_past_booking.html', {'form': form})


def cancel_booking(request, booking_id):
    try:
        booking = Booking.objects.get(id=booking_id)
        booking.cancel()  
        return redirect('user_dashboard')  # Redirect to the dashboard after cancellation
    except Booking.DoesNotExist:
        return render(request, 'error.html', {'message': 'Booking not found.'})



