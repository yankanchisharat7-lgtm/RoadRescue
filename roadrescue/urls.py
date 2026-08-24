from django.contrib import admin
from django.views.generic import TemplateView
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [

    # =========================================================
    # ADMIN
    # =========================================================

    path(
        "admin/",
        admin.site.urls
    ),


    # =========================================================
    # HOME
    # =========================================================

    path(
        "",
        include("core.urls")
    ),


    # =========================================================
    # ACCOUNTS
    # Customer Login
    # Customer Registration
    # Customer Dashboard
    # Mechanic Login
    # =========================================================

    path(
        "accounts/",
        include("accounts.urls")
    ),


    # =========================================================
    # MECHANICS
    # Mechanic List
    # Mechanic Details
    # Mechanic Dashboard
    # Mechanic Profile
    # =========================================================

    path(
        "mechanics/",
        include("mechanics.urls")
    ),


    # =========================================================
    # BOOKINGS
    # =========================================================

    path(
        "bookings/",
        include("bookings.urls")
    ),


    # =========================================================
    # REVIEWS
    # =========================================================

    path(
        "reviews/",
        include("reviews.urls")
    ),


    # =========================================================
    # NOTIFICATIONS
    # =========================================================

    path(
        "notifications/",
        include("notifications.urls")
    ),


    # =========================================================
    # ABOUT
    # =========================================================

    path(
        "about/",
        TemplateView.as_view(
            template_name="about.html"
        ),
        name="about"
    ),


    # =========================================================
    # CONTACT
    # =========================================================

    path(
        "contact/",
        TemplateView.as_view(
            template_name="contact.html"
        ),
        name="contact"
    ),

]


# =============================================================
# MEDIA FILES
# =============================================================

if settings.DEBUG:

    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )