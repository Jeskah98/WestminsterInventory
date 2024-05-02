from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from .models import Booking, Equipment

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['user', 'equipment', 'start_date', 'end_date', 'duration', 'purpose']  # Add start_date, end_date, and purpose
        widgets = {
            'purpose':forms.Textarea,
        }

class EquipmentForm(forms.ModelForm):
    class Meta:
        model = Equipment
        fields = ['name', 'type', 'quantity', 'location', 'availability', 'asset_tag', 'on_site_only']

class CustomUserCreationForm(UserCreationForm):
    role = forms.ChoiceField(choices=[('student', 'Student'), ('staff', 'Staff')])
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('role',) 

class CustomAuthenticationForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
