"""
Generic wrapper for financial info API
Meant to be extensible for any API host
Author: Ben Heney
UNHM, Spring 2024
"""

from abc import ABC, abstractmethod
from datetime import datetime


class APIWrapper(ABC):

    @abstractmethod
    def __init__(self):
        """
        Constructor. Implementation-specific
        """
        pass

    @abstractmethod
    def set_api_key(self, api_key: str):
        """
        Define an API key for the class. Implementation-specific.
        :param api_key: str, the API key
        """
        pass

    @abstractmethod
    def get_price_history(self, symbol, interval, start_date, end_date):
        """
        Get price history of an instrument
        :param symbol: str, the identifying symbol for the instrument
        :param interval: str, the resolution of the data
        :param start_date: datetime, the first data point
        :param end_date: datetime, the last data point
        :return: a list of tuples in the form of [ (datetime time, float price), ( etc ...) ]
            Each tuple represents a datapoint at frequency `interval`
        """
        if not isinstance(start_date, datetime) or not isinstance(end_date, datetime):
            raise APIWrapper.APIException("start_date and end_date must be datetime.datetime objects")

    class APIException(Exception):
        """
        Improper API usage
        """
        pass
