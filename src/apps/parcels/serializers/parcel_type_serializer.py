from rest_framework import serializers

from apps.parcels.models import ParcelType


class ParcelTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParcelType
        fields = [
            'id',
            'name',
        ]
