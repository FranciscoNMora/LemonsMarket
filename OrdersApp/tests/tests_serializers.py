from datetime import timedelta, datetime

from rest_framework.exceptions import ValidationError

from OrdersApp.models import Order
from OrdersApp.serializers import OrderSerializer, StockSerializer
from OrdersApp.tests.base_test import BaseTest
from OrdersApp.utils import utc_now, utc_timestamp


class OrderSerializersTest(BaseTest):
    @staticmethod
    def str_datetime(dt: datetime) -> str:
        return dt.strftime('%Y-%m-%d %H:%M:%S%Z')

    def save_serializer(self, raise_exception: bool = True) -> Order:
        s = OrderSerializer(data=self.data)
        s.is_valid(raise_exception=raise_exception)
        return s.save()

    def tests_serializer_create_order(self):
        o = self.save_serializer()
        self.assertIsInstance(o, Order)
        self.assertEqual(o.stock, self.apple)
        self.assertEqual(o.limit_price, self.data["limit_price"])
        self.assertTrue(o.side)
        self.assertEquals(o.quantity, 10)
        self.assertEqual(self.str_datetime(o.valid_until), self.str_datetime(self.valid))

    def tests_serializer_create_order_side_insensitive(self):
        self.data["side"] = "BUY"
        o1 = self.save_serializer()
        self.assertTrue(o1.side)
        self.data["side"] = "SELL"
        o2 = self.save_serializer()
        self.assertFalse(o2.side)
        self.data["side"] = "sell"
        o3 = self.save_serializer()
        self.assertFalse(o3.side)

    def tests_serializer_create_order_side_wrong(self):
        self.data["side"] = "BUYT"
        with self.assertRaises(ValidationError) as e:
            self.save_serializer()

    def tests_serializer_create_order_wrong_isin(self):
        self.data["isin"] = "NZ0000000000"
        with self.assertRaises(ValidationError):
            self.save_serializer()

    def tests_serializer_create_order_valid_until_in_the_past(self):
        self.data["valid_until"] = self.valid - timedelta(days=11)
        with self.assertRaises(ValidationError):
            self.save_serializer()

    def tests_serializer_create_order_negative_limit_price(self):
        self.data["limit_price"] = -100
        with self.assertRaises(ValidationError):
            self.save_serializer()


class StockSerializersTest(BaseTest):
    def tests_stock_serializer(self):
        data = StockSerializer(self.apple).data
        self._test_keys(data, ['isin', 'name'])
        self._test_values(data, {'isin': self.apple.isin, 'name': self.apple.name})
        #self.assertIn('isin', data)
        #self.assertIn('name', data)
        self.assertEqual(data['isin'], self.apple.isin)
        self.assertEqual(data['name'], self.apple.name)
