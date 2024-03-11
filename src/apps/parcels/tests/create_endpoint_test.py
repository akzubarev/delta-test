import logging
from unittest import mock
from uuid import UUID

from rest_framework.test import APITestCase
from apps.parcels.models import ParcelType, ParcelCandidate
from common.global_vars import PARCELS_KEY

logger = logging.getLogger(__name__)


class CreateParcelsTestCase(APITestCase):
    fixtures = [
        "parcel_types.json",
    ]
    url = '/api/v1/parcels/'

    correct_data = {
        "name": "Правильная посылка", "weight": 1.0,
        "price": 50.0, "type": 1,
    }

    @mock.patch('apps.parcels.tasks.register_parcel.delay')
    def test_endpoint(self, mock_delay):
        alterations = {
            "name": ["111111", 123, "_123_asdasdka"],
            "weight": [0.001, 0.1, 10, 100000000],
            "price": [0.001, 0.1, 10, 1000000002],
            "type": [1, 2, 3]
        }
        for field, error_cases in alterations.items():
            for err_case in error_cases:
                case_name = f"Правильные данные | {field} | {err_case}"
                with self.subTest(case_name):
                    still_correct_data = self.correct_data.copy()
                    if err_case is None:
                        still_correct_data.pop(field)
                    else:
                        still_correct_data.update({field: err_case})
                    response = self.client.post(
                        self.url, data=still_correct_data
                    )
                    data: dict = response.json()
                    parcel_uuid = UUID(data.get("uuid", None))
                    mock_delay.assert_called_with(ParcelCandidate(
                        name=str(still_correct_data["name"]),
                        weight=still_correct_data["weight"],
                        price=still_correct_data["price"], uuid=parcel_uuid,
                        type=still_correct_data["type"]
                    ))
                    self.assertIn(
                        parcel_uuid, self.client.session[PARCELS_KEY]
                    )

    def test_errors(self):
        alterations = {
            "name": [None, ""],
            "weight": [None, "20кг", -5.0, 0],
            "price": [None, "15 рублей", -200.2],
            "type": [None, "Разное", 0, ParcelType.objects.count() + 1, -1]
        }
        for field, error_cases in alterations.items():
            for err_case in error_cases:
                case_name = f"Неправильные данные | {field} | {err_case}"
                with self.subTest(case_name):
                    err_data = self.correct_data.copy()
                    if err_case is None:
                        err_data.pop(field)
                    else:
                        err_data.update({field: err_case})
                    response = self.client.post(self.url, data=err_data)
                    data: dict = response.json()
                    self.assertEquals(response.status_code, 400)
                    self.assertIsNotNone(data["errors"][field])
