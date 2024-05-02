from django.urls import path
from . import views
from . import adminviews

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.user_register, name='register'),
    path('login/', views.user_login, name='login'),
    path('pending_registrations/', adminviews.pending_registrations, name='pending_registrations'),
    path('registration_success/', views.registration_success, name='registration_success'),
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
    path('admin_dashboard/', adminviews.admin_dashboard, name='admin_dashboard'),
    path('equipment/', views.view_equipment, name='view_equipment'),
    path('equipment_list/', adminviews.equipment_list, name='equipment_list'),
    path('search/', views.search_equipment, name='search_equipment'),
    path('makebooking/<int:equipment_id>/', views.make_booking, name='make_booking'),
    path('booking-confirmation/', views.booking_confirmation, name='booking_confirmation'),
    path('approve_booking/<int:booking_id>/', adminviews.approve_booking, name='approve_booking'),
    path('reject_booking/<int:booking_id>/', adminviews.reject_booking, name='reject_booking'), 
    path('viewbookings/<int:equipment_id>/', views.view_bookings, name='view_bookings'),
    path('edit_equipment/<int:equipment_id>/', adminviews.edit_equipment, name='edit_equipment'),
    path('add_equipment/', adminviews.add_equipment, name='add_equipment'),
    path('delete_equipment/<int:equipment_id>/', adminviews.delete_equipment, name='delete_equipment'),
    path('pending_booking/', adminviews.pending_booking, name='pending_booking'),  
    path('users/', adminviews.list_users, name='user_list'),
    path('users/<int:user_id>/update_role/', adminviews.update_user_role, name='update_user_role'),
    path('users/<int:user_id>/delete/', adminviews.delete_user, name='delete_user'),
    path('add_user/', adminviews.add_user, name='add_user'),
    path('inventory_report/', adminviews.inventory_status_report, name='inventory_report'),
    path('equipment_report/', adminviews.equipment_usage_history, name='equipment_report'),
    path('return_booking/<int:booking_id>/', views.return_booking, name='return_booking'),
    path('book_from_past_booking/<int:booking_id>/', views.book_from_past_booking, name='book_from_past_booking'),
]
