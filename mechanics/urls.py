from django.urls import path
from . import views


urlpatterns = [

    # Mechanic List
    path(
        "",
        views.mechanic_list,
        name="mechanic_list"
    ),

    # Mechanic Details
    path(
        "<int:id>/",
        views.mechanic_detail,
        name="mechanic_detail"
    ),

    # Book Mechanic
    path(
        "<int:id>/book/",
        views.book_mechanic,
        name="book_mechanic"
    ),

    # Booking Success
    path(
        "success/",
        views.booking_success,
        name="booking_success"
    ),

    # Mechanic Dashboard
    path(
        "dashboard/",
        views.dashboard,
        name="mechanic_dashboard"
    ),

    # Update Booking Status
    path(
        "booking/<int:id>/update-status/",
        views.update_booking_status,
        name="update_booking_status"
    ),

    # Edit Mechanic Profile
    path(
        "profile/edit/",
        views.edit_profile,
        name="edit_mechanic_profile"
    ),

    # Toggle Availability
    path(
        "<int:id>/toggle-availability/",
        views.toggle_availability,
        name="toggle_availability"
    ),
]