import logging

from rest_framework.test import APITestCase
from apps.parcels.models import Parcel
from common.mixins.uuid_mixin import generate_uuid

logger = logging.getLogger(__name__)


class ClaimParcelTestCase(APITestCase):
    fixtures = [
        "parcel_types.json",
    ]
    url = "/api/v1/parcels/claim/"

    def setUp(self):
        self.parcel = Parcel.objects.create(
            name="Правильная посылка", weight=1, price=1, type_id=1,
            delivery_price=100
        )
        self.parcel_2 = Parcel.objects.create(
            name="Правильная посылка 2", weight=1, price=1, type_id=1
        )

    def test_errors(self):
        correct_data = {"uuid": self.parcel.uuid, "company_id": 1}
        alterations = {
            "uuid": [None, generate_uuid()],
            "company_id": [None, "Почти России", -5, 0, 5.5],
        }
        for field, error_cases in alterations.items():
            for err_case in error_cases:
                case_name = f"Неправильные данные | {field} | {err_case}"
                with self.subTest(case_name):
                    err_data = correct_data.copy()
                    if err_case is None:
                        err_data.pop(field)
                    else:
                        err_data.update({field: err_case})
                    response = self.client.post(self.url, err_data)
                    data: dict = response.json()
                    self.assertEquals(response.status_code, 400)
                    self.assertIsNotNone(data["errors"])

    def test_different(self):
        with self.subTest("Верно"):
            response = self.client.post(
                self.url, {"uuid": self.parcel.uuid, "company_id": 1}
            )
            data: dict = response.json()
            self.assertTrue(data["success"])

            response_2 = self.client.post(
                self.url, {"uuid": self.parcel_2.uuid, "company_id": 2}
            )
            data_2: dict = response_2.json()
            self.assertTrue(data_2["success"])

    def test_same(self):
        with self.subTest("Уже чья-то"):
            response_1 = self.client.post(
                self.url, {"uuid": self.parcel.uuid, "company_id": 1}
            )
            response_2 = self.client.post(
                self.url, {"uuid": self.parcel.uuid, "company_id": 1}
            )
            response_3 = self.client.post(
                self.url, {"uuid": self.parcel.uuid, "company_id": 2}
            )
            self.assertEquals(response_2.status_code, 403)
            self.assertEquals(response_3.status_code, 403)

            data_1: dict = response_1.json()
            data_2: dict = response_2.json()
            data_3: dict = response_3.json()
            self.assertTrue(data_1["success"])
            self.assertEquals(
                data_2["detail"], 'This parcel was already claimed'
            )
            self.assertEquals(
                data_3["detail"], 'This parcel was already claimed'
            )
