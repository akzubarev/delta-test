from rest_framework import serializers

from apps.parcels.models import Parcel


class ParcelSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    delivery_price = serializers.SerializerMethodField()
    company_id = serializers.SerializerMethodField()

    class Meta:
        model = Parcel
        fields = [
            # 'id',
            'uuid',
            'name',
            'price',
            'delivery_price',
            'weight',
            'type',
            'company_id',
        ]

    def get_type(self, parcel: Parcel):
        return parcel.type.name

    def get_delivery_price(self, parcel: Parcel):
        return parcel.delivery_price or "Не рассчитано"

    # в доп. задании не было прописано, что нужно это выводить и как,
    # но предполагаю, что вот так
    def get_company_id(self, parcel: Parcel):
        return parcel.company_id or "Не определено"


class ParcelCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parcel
        fields = [
            'name',
            'price',
            'weight',
            'type',
        ]
        extra_kwargs = {
            'name': {'required': True},
            'price': {'required': True},
            'weight': {'required': True},
            'type': {'required': True}
        }


class ParcelClaimSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField()

    class Meta:
        model = Parcel
        fields = [
            'uuid',
            'company_id',
        ]

        extra_kwargs = {
            'uuid': {'required': True},
            'company_id': {'required': True},
        }
