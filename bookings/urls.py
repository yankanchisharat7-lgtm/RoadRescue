from django.urls import path
from . import views

urlpatterns = [

    path(
        "book/<int:id>/",
        views.book_mechanic,
        name="book_mechanic"
    ),

    path(
        "my-bookings/",
        views.my_bookings,
        name="my_bookings"
    ),

    path(
        "detail/<int:id>/",
        views.booking_detail,
        name="booking_detail"
    ),

    path(
        "invoice/<int:id>/",
        views.download_invoice,
        name="download_invoice"
    ),

    path(
        "cancel/<int:id>/",
        views.cancel_booking,
        name="cancel_booking"
    ),

    path(
        "update-status/<int:id>/",
        views.update_status,
        name="update_status"
    ),
]
