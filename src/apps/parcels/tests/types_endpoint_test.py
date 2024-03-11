import logging

from rest_framework.test import APITestCase

logger = logging.getLogger(__name__)


class ParcelTypesTestCase(APITestCase):
    fixtures = [
        "parcel_types.json",
    ]
    url = '/api/v1/parcels/types/'

    def test_endpoint(self):
        response = self.client.get(self.url)
        data: list = response.json()
        self.assertEquals(len(data), 3)
        for parcel_type in data:
            self.assertIsNotNone(parcel_type["name"])
            self.assertIsNotNone(parcel_type["id"])
