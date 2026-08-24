from django.db import models
from django.contrib.auth.models import User
from mechanics.models import Mechanic


class Review(models.Model):
    customer = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    mechanic = models.ForeignKey(
        Mechanic,
        on_delete=models.CASCADE
    )

    rating = models.IntegerField()

    comment = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer.username} - {self.mechanic.shop_name}"