from django.db import models
from django.contrib.auth.models import User
from mechanics.models import Mechanic


class Booking(models.Model):
    STATUS = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('On The Way', 'On The Way'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]

    # Logged-in customer
    customer = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    customer_name = models.CharField(max_length=100)
    customer_phone = models.CharField(max_length=15)
    customer_location = models.CharField(max_length=200)

    mechanic = models.ForeignKey(Mechanic, on_delete=models.CASCADE)

    vehicle_type = models.CharField(max_length=50)
    problem = models.TextField()

    booking_date = models.DateTimeField(auto_now_add=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default='Pending'
    )

    def __str__(self):
        return f"{self.customer_name} - {self.mechanic.shop_name}"
    