from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.mail import send_mail

from .models import Mechanic
from .forms import MechanicProfileForm

from reviews.models import Review
from bookings.models import Booking
from notifications.models import Notification


def mechanic_list(request):

    mechanics = Mechanic.objects.all()

    search = request.GET.get("search")
    location = request.GET.get("location")
    vehicle = request.GET.get("vehicle")
    rating = request.GET.get("rating")
    available = request.GET.get("available")

    if search:
        mechanics = mechanics.filter(
            shop_name__icontains=search
        )

    if location:
        mechanics = mechanics.filter(
            location__icontains=location
        )

    if vehicle:
        mechanics = mechanics.filter(
            vehicle_type=vehicle
        )

    if rating:
        mechanics = mechanics.filter(
            rating__gte=float(rating)
        )

    if available:
        mechanics = mechanics.filter(
            available=True
        )

    return render(
        request,
        "mechanics/list.html",
        {
            "mechanics": mechanics,
        },
    )


def mechanic_detail(request, id):

    mechanic = get_object_or_404(
        Mechanic,
        id=id
    )

    reviews = Review.objects.filter(
        mechanic=mechanic
    ).order_by("-created_at")

    completed_jobs = Booking.objects.filter(
        mechanic=mechanic,
        status="Completed"
    ).count()

    return render(
        request,
        "mechanics/detail.html",
        {
            "mechanic": mechanic,
            "reviews": reviews,
            "completed_jobs": completed_jobs,
        },
    )


def book_mechanic(request, id):

    mechanic = get_object_or_404(
        Mechanic,
        id=id
    )

    return redirect(
        "mechanic_detail",
        id=mechanic.id
    )


def booking_success(request):

    return render(
        request,
        "mechanics/success.html"
    )


@login_required
def dashboard(request):

    mechanic = get_object_or_404(
        Mechanic,
        user=request.user
    )

    bookings = Booking.objects.filter(
        mechanic=mechanic
    ).order_by("-booking_date")

    total_jobs = bookings.count()

    pending_jobs = bookings.filter(
        status="Pending"
    ).count()

    accepted_jobs = bookings.filter(
        status="Accepted"
    ).count()

    on_the_way_jobs = bookings.filter(
        status="On The Way"
    ).count()

    completed_jobs = bookings.filter(
        status="Completed"
    ).count()

    cancelled_jobs = bookings.filter(
        status="Cancelled"
    ).count()

    return render(
        request,
        "mechanics/dashboard.html",
        {
            "mechanic": mechanic,
            "bookings": bookings,
            "total_jobs": total_jobs,
            "pending_jobs": pending_jobs,
            "accepted_jobs": accepted_jobs,
            "on_the_way_jobs": on_the_way_jobs,
            "completed_jobs": completed_jobs,
            "cancelled_jobs": cancelled_jobs,
        },
    )


@login_required
def update_booking_status(request, id):

    if request.method != "POST":
        return redirect("mechanic_dashboard")

    mechanic = get_object_or_404(
        Mechanic,
        user=request.user
    )

    booking = get_object_or_404(
        Booking,
        id=id,
        mechanic=mechanic
    )

    old_status = booking.status

    if booking.status == "Pending":

        booking.status = "Accepted"

        message = (
            f"Your booking with {mechanic.shop_name} "
            f"has been accepted."
        )

    elif booking.status == "Accepted":

        booking.status = "On The Way"

        message = (
            f"{mechanic.shop_name} is on the way "
            f"to your location."
        )

    elif booking.status == "On The Way":

        booking.status = "Completed"

        message = (
            f"Your service by {mechanic.shop_name} "
            f"has been completed."
        )

    else:

        return redirect("mechanic_dashboard")

    booking.save()

    Notification.objects.create(
        user=booking.customer,
        booking=booking,
        message=message
    )

    if booking.customer.email:

        send_mail(
            subject=(
                f"RoadRescue Booking Update - "
                f"{booking.status}"
            ),

            message=f"""
Hello {booking.customer.first_name or booking.customer.username},

Your RoadRescue booking has been updated.

Booking ID: RR-{booking.id:04d}

Mechanic: {mechanic.shop_name}

Vehicle: {booking.vehicle_type}

Problem: {booking.problem}

Previous Status: {old_status}

Current Status: {booking.status}

Thank you for choosing RoadRescue.

RoadRescue Team
""",

            from_email=settings.DEFAULT_FROM_EMAIL,

            recipient_list=[
                booking.customer.email
            ],

            fail_silently=True,
        )

    return redirect(
        "mechanic_dashboard"
    )


@login_required
def edit_profile(request):

    mechanic = get_object_or_404(
        Mechanic,
        user=request.user
    )

    if request.method == "POST":

        form = MechanicProfileForm(
            request.POST,
            request.FILES,
            instance=mechanic
        )

        if form.is_valid():

            form.save()

            return redirect(
                "mechanic_dashboard"
            )

    else:

        form = MechanicProfileForm(
            instance=mechanic
        )

    return render(
        request,
        "mechanics/edit_profile.html",
        {
            "form": form,
            "mechanic": mechanic,
        }
    )


@login_required
def toggle_availability(request, id):

    mechanic = get_object_or_404(
        Mechanic,
        id=id,
        user=request.user
    )

    mechanic.available = not mechanic.available

    mechanic.save()

    return redirect(
        "mechanic_dashboard"
    )