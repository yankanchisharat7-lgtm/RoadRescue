from django.shortcuts import render
from django.contrib.auth.models import User

from mechanics.models import Mechanic
from bookings.models import Booking
from reviews.models import Review


def home(request):
    # Dashboard Statistics
    total_customers = User.objects.count()
    total_mechanics = Mechanic.objects.count()
    total_bookings = Booking.objects.count()
    total_reviews = Review.objects.count()

    # Latest 3 Reviews
    latest_reviews = Review.objects.select_related(
        "customer",
        "mechanic"
    ).order_by("-created_at")[:3]

    context = {
        "total_customers": total_customers,
        "total_mechanics": total_mechanics,
        "total_bookings": total_bookings,
        "total_reviews": total_reviews,
        "latest_reviews": latest_reviews,
    }

    return render(request, "home.html", context)
