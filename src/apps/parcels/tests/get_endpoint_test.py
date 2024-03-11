import logging

from rest_framework.test import APITestCase
from apps.parcels.models import Parcel
from common.global_vars import PARCELS_KEY

logger = logging.getLogger(__name__)


class GetParcelTestCase(APITestCase):
    fixtures = [
        "parcel_types.json",
    ]
    url = "/api/v1/parcels/"

    def setUp(self):
        self.own_parcel = Parcel.objects.create(
            name="Правильная посылка", weight=1, price=1, type_id=1,
            delivery_price=100
        )
        self.own_parcel_2 = Parcel.objects.create(
            name="Правильная посылка", weight=1, price=1, type_id=1
        )
        self.other_parcel = Parcel.objects.create(
            name="Чужая посылка", weight=1, price=1, type_id=1
        )
        session = self.client.session
        session[PARCELS_KEY] = [
            self.own_parcel.uuid, self.own_parcel_2.uuid
        ]
        session.save()

    def test_endpoint(self):
        with self.subTest("Cвои посылки"):
            for parcel in [self.own_parcel, self.own_parcel_2]:
                response = self.client.get(self.url + f'{parcel.uuid}/')
                data: dict = response.json()
                self.assertEquals(parcel.name, data["name"])
                self.assertIsNotNone(parcel.uuid, data["uuid"])
                self.assertEquals(parcel.price, data["price"])
                self.assertEquals(parcel.weight, data["weight"])
                self.assertEquals(parcel.type.name, data["type"])
                self.assertEquals(
                    data["delivery_price"],
                    100 if parcel is self.own_parcel else "Не рассчитано"
                )

        with self.subTest("Чужая посылка"):
            response = self.client.get(self.url + f'{self.other_parcel.uuid}/')
            self.assertEquals(response.status_code, 403)
