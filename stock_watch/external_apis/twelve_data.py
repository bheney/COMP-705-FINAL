"""
An implementation of APIWrapper specific to the TwelveData API host
Author: Ben Heney
UNHM, Spring 2024
"""
from .api_wrapper import APIWrapper
from twelvedata import TDClient
from datetime import datetime, timezone


class TwelveData(APIWrapper):
    """
    Abstraction of the TwelveData API library compliant with the APIWrapper interface
    """

    def __init__(self):
        """
        Class constructor
        """
        super().__init__()
        self._key = None  # API key
        self._client = None  # API client object
        self.intervals = {  # Accepted intervals
            "1min",
            "5min",
            "15min",
            "30min",
            "45min",
            "1h",
            "2h",
            "4h",
            "8h",
            "1day",
            "1week",
            "1month"
        }

    def set_api_key(self, api_key: str):
        """
        Set the API Key.
        Has multiple side effects required for class construction
        :param api_key: str, A valid TwelveData  API key
        :return:
        """
        super().set_api_key(api_key)
        self._key = api_key
        self._client = TDClient(apikey=self._key)

    def get_price_history(self, symbol, interval, start_date, end_date):
        """
        Retrieve a dataset of instrument prices in a set window.
        :param symbol: str, instrument ID symbol
        :param interval: str, time between data points. See TwelveData.intervals
        :param start_date: datetime, first datum
        :param end_date: datetime, last datum
        :return: a list of tuples in the form of [ (datetime time, float price), ( etc ...) ]
            Each tuple represents a datapoint at frequency `interval`
        """
        # Validate parameters
        super().get_price_history(symbol, interval, start_date, end_date)
        if self._key is None:
            raise APIWrapper.APIException("No API key. TwelveData.set_api_key() not called.")
        if interval not in self.intervals:
            raise APIWrapper.APIException(f"Interval {interval} is not {self.intervals}")

        # Make the API Call
        time_series = self._client.time_series(
            symbol=symbol,
            interval=interval,
            start_date=start_date.astimezone(timezone.utc).strftime('%Y-%m-%d %H:%M:%S'),
            end_date=end_date.astimezone(timezone.utc).strftime('%Y-%m-%d %H:%M:%S'),
            timezone='UTC'
        )

        # Parse the JSON data into a list of tuples

        json_data = time_series.as_json()
        prepared_data = []
        for datum in json_data:
            time = self._parse_time(datum['datetime'])
            prepared_data.append((time, datum['close']))
        return prepared_data

    @staticmethod
    def _parse_time(time: str):
        """
        Parse a string of YYYY-MM-DD hh:mm:ss into a datetime object
        Assumes UTC
        :param time: sting YYYY-MM-DD hh:mm:ss
        :return: datetime
        """
        year = int(time[0:4])
        month = int(time[5:7])
        day = int(time[8:10])
        hour = int(time[11:13])
        minute = int(time[14:16])
        sec = int(time[17:19])

        return datetime(
            year=year,
            month=month,
            day=day,
            hour=hour,
            minute=minute,
            second=sec,
            microsecond=0,
            tzinfo=timezone.utc
        )