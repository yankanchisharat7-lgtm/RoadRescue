from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from mechanics.models import Mechanic
from reviews.models import Review

from .forms import BookingForm
from .models import Booking

from reportlab.pdfgen import canvas
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

@login_required
def book_mechanic(request, id):

    mechanic = get_object_or_404(
        Mechanic,
        id=id
    )

    # Do not allow booking an offline mechanic
    if not mechanic.available:

        return render(
            request,
            "bookings/not_available.html",
            {
                "mechanic": mechanic,
            }
        )

    if request.method == "POST":

        form = BookingForm(request.POST)

        if form.is_valid():

            booking = form.save(commit=False)

            # Logged-in customer
            booking.customer = request.user

            # Selected mechanic
            booking.mechanic = mechanic

            booking.save()


            # ==========================================
            # EMAIL TO CUSTOMER
            # ==========================================

            if request.user.email:

                send_mail(
                    subject="RoadRescue Booking Confirmation",

                    message=f"""
Hello {request.user.first_name or request.user.username},

Your RoadRescue booking has been successfully created.

Mechanic: {mechanic.shop_name}
Vehicle: {booking.vehicle_type}
Problem: {booking.problem}
Location: {booking.customer_location}
Booking Status: {booking.status}

Thank you for choosing RoadRescue.
""",

                    from_email=settings.DEFAULT_FROM_EMAIL,

                    recipient_list=[
                        request.user.email
                    ],

                    fail_silently=True,
                )


            # ==========================================
            # EMAIL TO MECHANIC
            # ==========================================

            if mechanic.email:

                send_mail(
                    subject="🚗 New RoadRescue Booking",

                    message=f"""
Hello {mechanic.shop_name},

You have received a new booking through RoadRescue.

CUSTOMER DETAILS
----------------
Name: {booking.customer_name}
Phone: {booking.customer_phone}
Location: {booking.customer_location}

VEHICLE DETAILS
---------------
Vehicle: {booking.vehicle_type}
Problem: {booking.problem}

BOOKING DETAILS
---------------
Booking ID: RR-{booking.id:04d}
Status: {booking.status}

Please login to your RoadRescue mechanic dashboard
to accept or manage this booking.

Thank you,
RoadRescue Team
""",

                    from_email=settings.DEFAULT_FROM_EMAIL,

                    recipient_list=[
                        mechanic.email
                    ],

                    fail_silently=True,
                )


            return redirect("booking_success")

    else:

        form = BookingForm()

    return render(
        request,
        "bookings/book.html",
        {
            "form": form,
            "mechanic": mechanic,
        }
    )


@login_required
def my_bookings(request):

    bookings = Booking.objects.filter(
        customer=request.user
    ).order_by("-booking_date")

    total_bookings = bookings.count()

    pending_bookings = bookings.filter(
        status="Pending"
    ).count()

    completed_bookings = bookings.filter(
        status="Completed"
    ).count()

    total_reviews = Review.objects.filter(
        customer=request.user
    ).count()

    return render(
        request,
        "bookings/my_bookings.html",
        {
            "bookings": bookings,
            "total_bookings": total_bookings,
            "pending_bookings": pending_bookings,
            "completed_bookings": completed_bookings,
            "total_reviews": total_reviews,
        }
    )


@login_required
def booking_detail(request, id):

    booking = get_object_or_404(
        Booking,
        id=id,
        customer=request.user
    )

    return render(
        request,
        "bookings/detail.html",
        {
            "booking": booking,
        }
    )

@login_required
def download_invoice(request, id):

    booking = get_object_or_404(
        Booking,
        id=id,
        customer=request.user
    )

    response = HttpResponse(
        content_type="application/pdf"
    )

    response["Content-Disposition"] = (
        f'attachment; filename="RoadRescue_Invoice_{booking.id}.pdf"'
    )

    pdf = canvas.Canvas(response, pagesize=A4)

    width, height = A4

    # Colors
    dark = colors.HexColor("#1F2937")
    primary = colors.HexColor("#2563EB")
    light = colors.HexColor("#F3F4F6")
    border = colors.HexColor("#D1D5DB")
    gray = colors.HexColor("#6B7280")
    green = colors.HexColor("#16A34A")

    # ---------------------------------------------------------
    # PAGE BORDER
    # ---------------------------------------------------------

    pdf.setStrokeColor(border)
    pdf.rect(
        30,
        30,
        width - 60,
        height - 60
    )

    # ---------------------------------------------------------
    # HEADER
    # ---------------------------------------------------------

    pdf.setFillColor(primary)
    pdf.rect(
        30,
        height - 125,
        width - 60,
        95,
        fill=1,
        stroke=0
    )

    pdf.setFillColor(colors.white)

    pdf.setFont(
        "Helvetica-Bold",
        24
    )

    pdf.drawString(
        50,
        height - 70,
        "RoadRescue"
    )

    pdf.setFont(
        "Helvetica",
        11
    )

    pdf.drawString(
        50,
        height - 92,
        "Professional Roadside Assistance"
    )

    pdf.setFont(
        "Helvetica-Bold",
        18
    )

    pdf.drawRightString(
        width - 50,
        height - 68,
        "SERVICE INVOICE"
    )

    pdf.setFont(
        "Helvetica",
        10
    )

    pdf.drawRightString(
        width - 50,
        height - 88,
        f"Invoice #RR-{booking.id:04d}"
    )

    # ---------------------------------------------------------
    # INVOICE DETAILS
    # ---------------------------------------------------------

    y = height - 155

    pdf.setFillColor(dark)
    pdf.setFont(
        "Helvetica-Bold",
        11
    )

    pdf.drawString(
        50,
        y,
        "INVOICE DETAILS"
    )

    y -= 22

    pdf.setFont(
        "Helvetica",
        10
    )

    pdf.setFillColor(gray)

    pdf.drawString(
        50,
        y,
        "Invoice Number"
    )

    pdf.setFillColor(dark)

    pdf.drawString(
        150,
        y,
        f"RR-{booking.id:04d}"
    )

    pdf.setFillColor(gray)

    pdf.drawString(
        330,
        y,
        "Booking Date"
    )

    pdf.setFillColor(dark)

    pdf.drawString(
        420,
        y,
        booking.booking_date.strftime(
            "%d-%m-%Y %I:%M %p"
        )
    )

    y -= 20

    pdf.setFillColor(gray)

    pdf.drawString(
        50,
        y,
        "Invoice Date"
    )

    pdf.setFillColor(dark)

    pdf.drawString(
        150,
        y,
        datetime.now().strftime(
            "%d-%m-%Y"
        )
    )

    pdf.setFillColor(gray)

    pdf.drawString(
        330,
        y,
        "Status"
    )

    pdf.setFillColor(green)

    pdf.setFont(
        "Helvetica-Bold",
        10
    )

    pdf.drawString(
        420,
        y,
        str(booking.status).upper()
    )

    # ---------------------------------------------------------
    # CUSTOMER / MECHANIC SECTION
    # ---------------------------------------------------------

    y -= 40

    pdf.setFillColor(light)

    pdf.roundRect(
        45,
        y - 100,
        240,
        100,
        6,
        fill=1,
        stroke=0
    )

    pdf.roundRect(
        305,
        y - 100,
        240,
        100,
        6,
        fill=1,
        stroke=0
    )

    # Customer
    pdf.setFillColor(primary)

    pdf.setFont(
        "Helvetica-Bold",
        11
    )

    pdf.drawString(
        60,
        y - 22,
        "CUSTOMER INFORMATION"
    )

    pdf.setFillColor(dark)

    pdf.setFont(
        "Helvetica",
        10
    )

    pdf.drawString(
        60,
        y - 45,
        f"Name: {booking.customer_name}"
    )

    pdf.drawString(
        60,
        y - 63,
        f"Phone: {booking.customer_phone}"
    )

    # Mechanic
    pdf.setFillColor(primary)

    pdf.setFont(
        "Helvetica-Bold",
        11
    )

    pdf.drawString(
        320,
        y - 22,
        "MECHANIC INFORMATION"
    )

    pdf.setFillColor(dark)

    pdf.setFont(
        "Helvetica",
        10
    )

    pdf.drawString(
        320,
        y - 45,
        f"Shop: {booking.mechanic.shop_name}"
    )

    pdf.drawString(
        320,
        y - 63,
        "Service Provider: RoadRescue"
    )

    # ---------------------------------------------------------
    # VEHICLE / SERVICE DETAILS
    # ---------------------------------------------------------

    y -= 130

    pdf.setFillColor(dark)

    pdf.setFont(
        "Helvetica-Bold",
        12
    )

    pdf.drawString(
        50,
        y,
        "SERVICE DETAILS"
    )

    y -= 20

    # Table header
    pdf.setFillColor(primary)

    pdf.roundRect(
        45,
        y - 30,
        510,
        30,
        4,
        fill=1,
        stroke=0
    )

    pdf.setFillColor(colors.white)

    pdf.setFont(
        "Helvetica-Bold",
        10
    )

    pdf.drawString(
        60,
        y - 20,
        "DESCRIPTION"
    )

    pdf.drawString(
        390,
        y - 20,
        "VEHICLE"
    )

    pdf.drawRightString(
        540,
        y - 20,
        "STATUS"
    )

    y -= 45

    pdf.setFillColor(dark)

    pdf.setFont(
        "Helvetica",
        10
    )

    pdf.drawString(
        60,
        y,
        "Roadside Assistance Service"
    )

    pdf.drawString(
        390,
        y,
        str(booking.vehicle_type)
    )

    pdf.setFillColor(green)

    pdf.setFont(
        "Helvetica-Bold",
        10
    )

    pdf.drawRightString(
        540,
        y,
        str(booking.status).upper()
    )

    # ---------------------------------------------------------
    # PROBLEM
    # ---------------------------------------------------------

    y -= 40

    pdf.setFillColor(dark)

    pdf.setFont(
        "Helvetica-Bold",
        11
    )

    pdf.drawString(
        50,
        y,
        "SERVICE REQUEST"
    )

    y -= 20

    pdf.setFillColor(gray)

    pdf.setFont(
        "Helvetica",
        10
    )

    problem = str(
        booking.problem
    )

    # Wrap long problem text
    problem_lines = []

    while len(problem) > 75:
        split_at = problem.rfind(
            " ",
            0,
            75
        )

        if split_at == -1:
            split_at = 75

        problem_lines.append(
            problem[:split_at]
        )

        problem = problem[
            split_at:
        ].strip()

    if problem:
        problem_lines.append(problem)

    for line in problem_lines:
        pdf.drawString(
            60,
            y,
            line
        )
        y -= 15

    # ---------------------------------------------------------
    # LOCATION
    # ---------------------------------------------------------

    y -= 15

    pdf.setFillColor(dark)

    pdf.setFont(
        "Helvetica-Bold",
        11
    )

    pdf.drawString(
        50,
        y,
        "SERVICE LOCATION"
    )

    y -= 20

    pdf.setFillColor(gray)

    pdf.setFont(
        "Helvetica",
        10
    )

    location = str(
        booking.customer_location
    )

    location_lines = []

    while len(location) > 75:
        split_at = location.rfind(
            " ",
            0,
            75
        )

        if split_at == -1:
            split_at = 75

        location_lines.append(
            location[:split_at]
        )

        location = location[
            split_at:
        ].strip()

    if location:
        location_lines.append(location)

    for line in location_lines:
        pdf.drawString(
            60,
            y,
            line
        )
        y -= 15

    # ---------------------------------------------------------
    # TOTAL / SUMMARY
    # ---------------------------------------------------------

    y -= 30

    pdf.setStrokeColor(border)

    pdf.line(
        45,
        y,
        555,
        y
    )

    y -= 30

    pdf.setFillColor(light)

    pdf.roundRect(
        350,
        y - 65,
        195,
        65,
        6,
        fill=1,
        stroke=0
    )

    pdf.setFillColor(dark)

    pdf.setFont(
        "Helvetica-Bold",
        11
    )

    pdf.drawString(
        365,
        y - 22,
        "SERVICE STATUS"
    )

    pdf.setFillColor(green)

    pdf.setFont(
        "Helvetica-Bold",
        14
    )

    pdf.drawRightString(
        530,
        y - 48,
        str(booking.status).upper()
    )

    # ---------------------------------------------------------
    # FOOTER
    # ---------------------------------------------------------

    pdf.setFillColor(primary)

    pdf.line(
        50,
        75,
        width - 50,
        75
    )

    pdf.setFillColor(dark)

    pdf.setFont(
        "Helvetica-Bold",
        11
    )

    pdf.drawCentredString(
        width / 2,
        57,
        "Thank you for choosing RoadRescue!"
    )

    pdf.setFont(
        "Helvetica",
        9
    )

    pdf.setFillColor(gray)

    pdf.drawCentredString(
        width / 2,
        43,
        "Drive safely. RoadRescue is always here when you need us."
    )

    pdf.drawCentredString(
        width / 2,
        30,
        "This is a computer-generated invoice."
    )

    # ---------------------------------------------------------
    # SAVE
    # ---------------------------------------------------------

    pdf.save()

    return response

@login_required
def cancel_booking(request, id):

    booking = get_object_or_404(
        Booking,
        id=id,
        customer=request.user
    )

    # Customers can cancel only Pending bookings
    if booking.status == "Pending":

        booking.status = "Cancelled"

        booking.save()

    return redirect(
        "my_bookings"
    )

@login_required
def update_status(request, id):

    booking = get_object_or_404(
        Booking,
        id=id
    )

    # Only the mechanic assigned to this booking can update it
    if booking.mechanic.user != request.user:
        return redirect("dashboard")

    if booking.status == "Pending":

        booking.status = "Accepted"

    elif booking.status == "Accepted":

        booking.status = "Completed"

    booking.save()

    return redirect("dashboard")

