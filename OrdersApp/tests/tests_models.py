from datetime import timedelta, datetime

from django.db import IntegrityError

from OrdersApp.models import Stock, Order
from OrdersApp.tests.base_test import BaseTest
from OrdersApp.utils import utc_now


class ModelsTest(BaseTest):
    def test_create_stock(self):
        s = Stock.objects.create(isin='ES0144580Y14', name='Iberdrola S.A.')
        self.assertEqual(str(s), 'Iberdrola S.A.')
        self.assertEqual(s.name, 'Iberdrola S.A.')
        self.assertEqual(s.isin, 'ES0144580Y14')

    def test_create_stock_repited_isin(self):
        with self.assertRaises(IntegrityError):
            s = Stock.objects.create(isin=self.apple.isin, name='Company Inc.')

    def test_create_stock_repited_name(self):
        with self.assertRaises(IntegrityError):
            s = Stock.objects.create(isin='NZ0144580Y14', name=self.apple.name)

    def test_create_order(self):
        valid = utc_now() + timedelta(days=1)
        o = Order.objects.create(
            stock=self.apple,
            limit_price=100.35,
            side=True,
            valid_until=valid,
            quantity=10,
        )
        self.assertEqual(str(o), 'buy 10 x Apple, Inc.')
        self.assertIsInstance(o.created, datetime)
        self.assertEqual(o.limit_price, 100.35)
        self.assertEqual(o.valid_until, valid)

    def test_create_order_negative_quantity(self):
        valid = utc_now() + timedelta(days=1)
        with self.assertRaises(IntegrityError):
            o = Order.objects.create(
                stock=self.apple,
                limit_price=100,
                side=True,
                valid_until=valid,
                quantity=-10,
            )
