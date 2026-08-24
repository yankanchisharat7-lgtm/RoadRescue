from django.contrib import admin
from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "user",
        "booking",
        "message",
    )

    list_filter = (
        "user",
    )

    search_fields = (
        "user__username",
        "message",
    )

    ordering = (
        "-id",
    )
    