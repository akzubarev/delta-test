import logging
from uuid import UUID

from rest_framework.test import APITestCase
from apps.parcels.models import Parcel
from common.global_vars import PARCELS_KEY

logger = logging.getLogger(__name__)


class ListParcelsTestCase(APITestCase):
    fixtures = [
        "parcel_types.json",
    ]
    url = '/api/v1/parcels/'

    def setUp(self):
        self.own_parcel = Parcel.objects.create(
            name="Правильная посылка", weight=1, price=1, type_id=1,
            delivery_price=100
        )
        self.own_parcel_2 = Parcel.objects.create(
            name="Правильная посылка 2", weight=1, price=1, type_id=2
        )
        self.other_parcel = Parcel.objects.create(
            name="Чужая посылка", weight=1, price=1, type_id=1
        )
        self.session = self.client.session
        self.session[PARCELS_KEY] = {
            self.own_parcel.uuid, self.own_parcel_2.uuid
        }
        self.session.save()

    def test_endpoint(self):
        response = self.client.get(self.url)
        data: list = response.json()
        self.assertEquals(len(data), 2)
        for parcel in data:
            self.assertIsNotNone(parcel["name"])
            self.assertIsNotNone(parcel["uuid"])
            self.assertIsNotNone(parcel["weight"])
            self.assertIsNotNone(parcel["price"])
            self.assertIsNotNone(parcel["type"])
            self.assertNotEquals(parcel["uuid"], self.other_parcel.uuid)
            self.assertEquals(
                parcel["delivery_price"], 100 if
                UUID(parcel[
                         "uuid"]) == self.own_parcel.uuid else "Не рассчитано"
            )

    def test_filtering(self):
        with self.subTest("without"):
            response = self.client.get(self.url)
            data: list = response.json()
            self.assertEquals(len(data), 2)
            self.assertIsNotNone(UUID(data[0]["uuid"]), self.own_parcel.uuid)
            self.assertIsNotNone(UUID(data[1]["uuid"]), self.own_parcel_2.uuid)

        with self.subTest("filter_delivery"):
            response = self.client.get(self.url + "?delivery=true")
            data: list = response.json()
            self.assertEquals(len(data), 1)
            self.assertEquals(UUID((data[0]["uuid"])), self.own_parcel.uuid)

        with self.subTest("filter_type"):
            response = self.client.get(self.url + "?type=2")
            data: list = response.json()
            self.assertEquals(len(data), 1)
            self.assertEquals(UUID(data[0]["uuid"]), self.own_parcel_2.uuid)

        with self.subTest("filter_both"):
            response = self.client.get(self.url + "?type=2&delivery=true")
            data: list = response.json()
            self.assertEquals(len(data), 0)

    def test_pagination(self):
        with self.subTest("without"):
            response = self.client.get(self.url)
            data: list = response.json()
            self.assertEquals(len(data), 2)
            self.assertEquals(UUID(data[0]["uuid"]), self.own_parcel.uuid)
            self.assertEquals(UUID(data[1]["uuid"]), self.own_parcel_2.uuid)

        with self.subTest("limit"):
            response = self.client.get(self.url + "?limit=1")
            data: list = response.json()
            self.assertEquals(len(data), 1)
            self.assertIsNotNone(UUID(data[0]["uuid"]), self.own_parcel.uuid)

        with self.subTest("limit_0"):
            response = self.client.get(self.url + "?limit=0")
            data: list = response.json()
            self.assertEquals(len(data), 2)

        with self.subTest("offset"):
            response = self.client.get(self.url + "?offset=1")
            data: list = response.json()
            self.assertEquals(len(data), 1)
            self.assertIsNotNone(UUID(data[0]["uuid"]), self.own_parcel_2.uuid)

        with self.subTest("limit+offset"):
            self.session[PARCELS_KEY] = {
                self.own_parcel.uuid, self.own_parcel_2.uuid, self.other_parcel
            }
            response = self.client.get(self.url)
            data: list = response.json()
            self.assertEquals(len(data), 2)

            response = self.client.get(self.url + "?limit=1&offset=1")
            data: list = response.json()
            self.assertEquals(len(data), 1)
            self.assertIsNotNone(UUID(data[0]["uuid"]), self.own_parcel.uuid)
