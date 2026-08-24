from django.db import models
from django.contrib.auth.models import User


class Mechanic(models.Model):

    # Link mechanic with Django User
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    VEHICLE_CHOICES = [
        ('Bike', 'Bike'),
        ('Car', 'Car'),
        ('Truck', 'Truck'),
        ('EV', 'Electric Vehicle'),
    ]

    name = models.CharField(max_length=100)
    shop_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    location = models.CharField(max_length=200)
    experience = models.PositiveIntegerField()
    vehicle_type = models.CharField(max_length=20, choices=VEHICLE_CHOICES)
    available = models.BooleanField(default=True)

    inspection_charge = models.DecimalField(max_digits=8, decimal_places=2)
    battery_charge = models.DecimalField(max_digits=8, decimal_places=2)
    tyre_change_charge = models.DecimalField(max_digits=8, decimal_places=2)
    engine_repair_charge = models.DecimalField(max_digits=8, decimal_places=2)
    oil_change_charge = models.DecimalField(max_digits=8, decimal_places=2)
    brake_repair_charge = models.DecimalField(max_digits=8, decimal_places=2)
    towing_charge_per_km = models.DecimalField(max_digits=8, decimal_places=2)

    rating = models.FloatField(default=0)

    def __str__(self):
        return self.shop_name
    
    photo = models.ImageField(
    upload_to="mechanics/",
    blank=True,
    null=True
)
    