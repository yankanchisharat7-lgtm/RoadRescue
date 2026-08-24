from django.contrib import admin
from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "customer",
        "mechanic",
        "vehicle_type",
        "booking_date",
        "status",
    )

    list_filter = (
        "status",
        "booking_date",
    )

    search_fields = (
        "customer__username",
        "customer__email",
        "mechanic__name",
        "mechanic__shop_name",
        "vehicle_type",
        "problem",
    )

    ordering = (
        "-booking_date",
    )
    