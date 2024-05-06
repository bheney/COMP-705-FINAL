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
    def get_latest_price_history(self, symbol=None, interval=None, data_points=None):
        """
        Get price history of an instrument
        :param symbol: str, the identifying symbol for the instrument
        :param interval: str, the resolution of the data
        :param start_date: datetime, the first data point
        :param end_date: datetime, the last data point
        :param data_points: int, the number of points in the returned data set
        :return: a list of tuples in the form of [ (datetime time, float price), ( etc ...) ]
            Each tuple represents a datapoint at frequency `interval`
        """

    @abstractmethod
    def get_price_history(self, symbol=None, interval=None, start_date=None, end_date=None,
                                 data_points=None):
        """
        Get price history of an instrument
        :param symbol: str, the identifying symbol for the instrument
        :param interval: str, the resolution of the data
        :param start_date: datetime, the first data point
        :param end_date: datetime, the last data point
        :param data_points: int, the number of points in the returned data set
        :return: a list of tuples in the form of [ (datetime time, float price), ( etc ...) ]
            Each tuple represents a datapoint at frequency `interval`
        """
        if start_date is not None and not isinstance(start_date, datetime):
            raise APIWrapper.APIException("start_date must be datetime.datetime object")
        if end_date is not None and not isinstance(end_date, datetime):
            raise APIWrapper.APIException("end_date must be datetime.datetime object")
    class APIException(Exception):
        """
        Improper API usage
        """
        pass
