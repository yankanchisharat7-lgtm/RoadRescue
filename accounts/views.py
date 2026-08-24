from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.db import transaction

from .forms import RegisterForm
from mechanics.models import Mechanic


def register(request):

    if request.method == "POST":

        form = RegisterForm(request.POST)

        if form.is_valid():

            with transaction.atomic():

                user = form.save()

                account_type = form.cleaned_data["account_type"]

                if account_type == "mechanic":

                    Mechanic.objects.get_or_create(
                        user=user,
                        defaults={
                            "name": (
                                f"{user.first_name} "
                                f"{user.last_name}"
                            ).strip() or user.username,

                            "shop_name": (
                                f"{user.username}'s Garage"
                            ),

                            "phone": "0000000000",

                            "email": user.email,

                            "location": "Not Updated",

                            "experience": 0,

                            "vehicle_type": "Car",

                            "available": True,

                            "inspection_charge": 0,

                            "battery_charge": 0,

                            "tyre_change_charge": 0,

                            "engine_repair_charge": 0,

                            "oil_change_charge": 0,

                            "brake_repair_charge": 0,

                            "towing_charge_per_km": 0,

                            "rating": 0,
                        }
                    )

                login(request, user)

                if account_type == "mechanic":
                    return redirect("mechanic_dashboard")

                return redirect("dashboard")

    else:

        form = RegisterForm()

    return render(
        request,
        "accounts/register.html",
        {
            "form": form
        }
    )


def user_login(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            if Mechanic.objects.filter(
                user=user
            ).exists():

                return render(
                    request,
                    "accounts/login.html",
                    {
                        "login_type": "user",
                        "error": (
                            "This account is registered as a "
                            "mechanic. Please use Mechanic Login."
                        )
                    }
                )

            login(request, user)

            return redirect("dashboard")

        return render(
            request,
            "accounts/login.html",
            {
                "login_type": "user",
                "error": (
                    "Invalid customer username or password."
                )
            }
        )

    return render(
        request,
        "accounts/login.html",
        {
            "login_type": "user"
        }
    )


def mechanic_login(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            if not Mechanic.objects.filter(
                user=user
            ).exists():

                return render(
                    request,
                    "accounts/login.html",
                    {
                        "login_type": "mechanic",
                        "error": (
                            "This account is not registered "
                            "as a mechanic."
                        )
                    }
                )

            login(request, user)

            return redirect("mechanic_dashboard")

        return render(
            request,
            "accounts/login.html",
            {
                "login_type": "mechanic",
                "error": (
                    "Invalid mechanic username or password."
                )
            }
        )

    return render(
        request,
        "accounts/login.html",
        {
            "login_type": "mechanic"
        }
    )


def user_logout(request):

    logout(request)

    return redirect("/")


@login_required
def dashboard(request):

    # Prevent mechanics from accessing customer dashboard
    if Mechanic.objects.filter(
        user=request.user
    ).exists():

        return redirect("mechanic_dashboard")

    from bookings.models import Booking
    from reviews.models import Review
    from notifications.models import Notification

    bookings = Booking.objects.filter(
        customer=request.user
    )

    total_bookings = bookings.count()

    pending_bookings = bookings.filter(
        status="Pending"
    ).count()

    accepted_bookings = bookings.filter(
        status="Accepted"
    ).count()

    on_the_way_bookings = bookings.filter(
        status="On The Way"
    ).count()

    completed_bookings = bookings.filter(
        status="Completed"
    ).count()

    cancelled_bookings = bookings.filter(
        status="Cancelled"
    ).count()

    total_reviews = Review.objects.filter(
        customer=request.user
    ).count()

    unread_notifications = Notification.objects.filter(
        user=request.user,
        is_read=False
    ).count()

    recent_bookings = bookings.select_related(
        "mechanic"
    ).order_by(
        "-booking_date"
    )[:5]

    return render(
        request,
        "accounts/dashboard.html",
        {
            "total_bookings": total_bookings,
            "pending_bookings": pending_bookings,
            "accepted_bookings": accepted_bookings,
            "on_the_way_bookings": on_the_way_bookings,
            "completed_bookings": completed_bookings,
            "cancelled_bookings": cancelled_bookings,
            "total_reviews": total_reviews,
            "unread_notifications": unread_notifications,
            "recent_bookings": recent_bookings,
        }
    )