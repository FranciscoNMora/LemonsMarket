from datetime import datetime

import pytz
from django.test import TestCase

from OrdersApp.utils import utc_now, utc_timestamp, utc_datetime


class UtilsTest(TestCase):
    def test_utc_now(self):
        now = utc_now()
        self.assertIsInstance(now, datetime, f"utc_now() returns {type(now)}")
        self.assertEqual(now.tzinfo, pytz.utc, "utc_now() timezone is not UTC")

    def test_utc_timestamp(self):
        t1 = datetime(2021, 5, 23, 10, 26, 31, 5018)
        self.assertEqual(utc_timestamp(t1), 1621765591)
        t2 = pytz.utc.localize(t1)
        self.assertEqual(utc_timestamp(t2), 1621765591)
        t3 = pytz.timezone('Europe/Berlin').localize(t1)
        self.assertEqual(utc_timestamp(t3), 1621758391)

    def test_utc_datetime(self):
        timestamp = 1621765591
        t = pytz.utc.localize(datetime(2021, 5, 23, 10, 26, 31))
        self.assertEqual(utc_datetime(timestamp), t)

