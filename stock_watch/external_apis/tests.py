from django.test import TestCase
from .twelve_data import (TwelveData)
from decouple import config
from datetime import datetime, timezone, timedelta


class TwelveDataTestCase(TestCase):
    MAX_DATA = 30

    def test_TJX_last_open(self):
        # Spin up the API interface
        api_client = TwelveData()
        api_client.set_api_key(config('TWELVE_DATA_API_KEY'))

        # Determine the last opening bell on the NASDAQ
        now = datetime.now(timezone.utc)
        open_today = now.replace(hour=13, minute=0, second=0, microsecond=0)
        if now < open_today:
            last_open = open_today - timedelta(days=1)
        else:
            last_open = open_today

        # Check the output of the API call
        tjx_history = api_client.get_price_history('TJX', '1min', last_open, now)

        # Check length
        window = now - last_open
        assert len(tjx_history) == min(int(window.total_seconds() / 60), self.MAX_DATA) # Returned data limited to 30 datapoints

        # Check types
        assert isinstance(tjx_history[0][0], datetime)
        if len(tjx_history) < self.MAX_DATA:
            assert last_open - timedelta(minutes=1) <= tjx_history[-1][0] <= last_open
        else:
            assert last_open -timedelta(minutes=self.MAX_DATA+1) <= tjx_history[-1][0] <= now - timedelta(minutes=self.MAX_DATA)
        assert now - timedelta(minutes=1) <= tjx_history[0][0] <= now
        assert isinstance(tjx_history[0][1], float)


if __name__=='__main__':
    test = TwelveDataTestCase()
    test.test_TJX_last_open()