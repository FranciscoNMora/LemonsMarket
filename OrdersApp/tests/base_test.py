from datetime import timedelta
from typing import Any, List, Dict

from django.test import TransactionTestCase

from OrdersApp.models import Stock
from OrdersApp.utils import utc_now, utc_timestamp


class BaseTest(TransactionTestCase):
    fixtures = ["stocks.yaml"]

    def setUp(self) -> None:
        self.apple = Stock.objects.get(isin='US0378331005')
        self.volkswagen = Stock.objects.get(isin='DE0007664039')
        self.valid = utc_now() + timedelta(days=10)
        self.data = {
            "isin": self.apple.isin,
            "limit_price": 100.35,
            "side": "buy",
            "valid_until": utc_timestamp(self.valid),
            "quantity": 10
        }

    def _test_keys(self, obj: Any, keys: List[str], *, exclude: List[str] = []):
        for key in keys:
            self.assertIn(key, obj)
        for key in exclude:
            self.assertNotIn(key, obj)

    def _test_values(self, obj: Dict[str, Any], expected: Dict[str, Any]):
        for key, value in expected.items():
            self.assertEqual(obj[key], expected[key])
