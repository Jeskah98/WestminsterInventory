# Generated by Django 5.0.4 on 2024-05-01 02:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_name', '0006_remove_equipment_return_date_alter_booking_end_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='returned',
            field=models.BooleanField(default=False),
        ),
    ]