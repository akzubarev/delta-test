from django.contrib import admin

from apps.parcels.models import Parcel


@admin.register(Parcel)
class ParcelAdmin(admin.ModelAdmin):
    list_display = [
        # 'id',
        'name',
        'weight',
        'price',
        'type',
        'delivery_price',
        'company_id',
    ]
