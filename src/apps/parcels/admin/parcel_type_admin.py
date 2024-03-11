from django.contrib import admin

from apps.parcels.models import ParcelType


@admin.register(ParcelType)
class ParcelTypeAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
    ]
