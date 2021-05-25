from datetime import timedelta
from typing import Dict, Any

from django.urls import reverse

from OrdersApp.models import Order
from OrdersApp.tests.base_test import BaseTest

from rest_framework.test import APIClient

from OrdersApp.utils import utc_timestamp


class StockAPITests(BaseTest):
    def setUp(self):
        super().setUp()
        self.unauth_client = APIClient()

    def test_list_stocks(self):
        url = reverse('stocks-api-v1')
        resp = self.unauth_client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.data), 10)
        for user in resp.data:
            self._test_keys(user, ['isin', 'name'])


class OrdersAPITests(BaseTest):
    def setUp(self):
        super().setUp()
        self.unauth_client = APIClient()

    def test_post_orders(self):
        url = reverse('orders-api-v1')
        resp = self.unauth_client.post(url, self.data, format='json')
        self.assertEqual(resp.status_code, 201)
        self.assertTrue(Order.objects.filter(uuid=resp.data.get('order_uuid')))

    def _test_side(self, *, side: bool):
        url = reverse('orders-api-v1')
        resp = self.unauth_client.post(url, self.data, format='json')
        self.assertEqual(resp.status_code, 201)
        uuid = resp.data.get('order_uuid')
        self.assertTrue(Order.objects.filter(uuid=uuid))
        o = Order.objects.get(uuid=uuid)
        self.assertEqual(o.side, side)

    def test_post_orders_insensitive_side(self):
        self.data["side"] = "BUY"
        self._test_side(side=True)
        self.data["side"] = "sell"
        self._test_side(side=False)
        self.data["side"] = "SELL"
        self._test_side(side=False)

    def _test_error_message(self, *, field, message):
        url = reverse('orders-api-v1')
        resp = self.unauth_client.post(url, self.data, format='json')
        self.assertEqual(resp.status_code, 400)
        self.assertIn(field, resp.data)
        self.assertEqual(str(resp.data[field][0]), message)

    def test_post_orders_wrong_side(self):
        self.data["side"] = "BUYt"
        self._test_error_message(field='side', message="side must be 'buy' or 'sell'")

    def test_post_orders_wrong_isin(self):
        self.data["isin"] = "NZ0000000000"
        self._test_error_message(field='isin', message="Stock ISIN does not exist")

    def test_post_orders_valid_until_in_the_past(self):
        self.data["valid_until"] = utc_timestamp(self.valid - timedelta(days=11))
        self._test_error_message(field='valid_until', message="valid_until is in the past")

    def test_post_orders_negative_limit_price(self):
        self.data["limit_price"] = -100
        self._test_error_message(field='limit_price', message="Ensure this value is greater than or equal to 0.")



