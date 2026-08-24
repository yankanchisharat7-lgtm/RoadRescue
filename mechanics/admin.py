from django.contrib import admin
from .models import Mechanic


@admin.register(Mechanic)
class MechanicAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name",
        "shop_name",
        "location",
        "phone",
        "rating",
        "available",
    )

    list_filter = (
        "available",
        "location",
    )

    search_fields = (
        "name",
        "shop_name",
        "location",
        "phone",
    )