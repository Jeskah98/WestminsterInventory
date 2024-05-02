from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

class User(AbstractUser):
    role_choices = [
        ('student', 'Student'),
        ('staff', 'Staff')
    ]
    role = models.CharField(max_length=10, choices=role_choices)
    class Meta:
        app_label = 'main_name'

 
    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        related_name='main_name_users_groups',
        related_query_name='user_main_name_groups',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        related_name='main_name_users_permissions',
        related_query_name='user_main_name_permissions',
    )

class Admin(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.EmailField()

class Equipment(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    quantity = models.IntegerField(default=0)
    location = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    availability = models.BooleanField(default=True)
    asset_tag = models.CharField(max_length=100)
    on_site_only = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    date = models.DateField()

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    duration = models.IntegerField(default=0)  
    purpose = models.TextField(default='General purpose') 
    returned = models.BooleanField(default=False) 
    STATUS_PENDING = 'pending'
    STATUS_APPROVED = 'approved'
    STATUS_REJECTED = 'rejected'
    STATUS_CANCELLED = 'cancelled'
    
    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_APPROVED, 'Approved'),
        (STATUS_REJECTED, 'Rejected'),
        (STATUS_CANCELLED, 'Cancelled'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    
    def cancel(self):
        self.status = 'cancelled'
        self.save()
        self.equipment.quantity += 1 
        self.equipment.save()


class Report(models.Model):
    report_type = models.CharField(max_length=100)
    date = models.DateField()
