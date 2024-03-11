from django_filters import rest_framework as drf_filters

from apps.parcels.models import Parcel


class ParcelFilter(drf_filters.FilterSet):
    type = drf_filters.NumberFilter(field_name="type__id", lookup_expr='exact')
    delivery = drf_filters.BooleanFilter(
        field_name="delivery_price", lookup_expr='isnull', exclude=True
    )

    class Meta:
        model = Parcel
        fields = ['type', 'delivery']
