import datetime

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from external_apis.twelve_data import TwelveData
from decouple import config

class Stock(models.Model):
    symbol = models.CharField(max_length=settings.MAX_SYMBOL_LENGTH)
    name = models.CharField(max_length=256)
    exchange = models.CharField(max_length=256)
    last_refresh = models.DateTimeField()
    api = TwelveData()
    api.set_api_key(config("TWELVE_DATA_API_KEY"))

    def __eq__(self, other):
        if isinstance(other, Stock):
            return self.symbol == other.symbol
        elif isinstance(other, str):
            return self.symbol == other
        else:
            return NotImplemented

    def __str__(self):
        return self.symbol

    def update(self):
        # TODO: Set up logging/error management for the API calls
        new_data = self.api.get_latest_price_history(symbol=self.symbol, interval=settings.API_MIN_RESOLUTION)
        for (time, price) in new_data:
            PriceData.add(self, price, time)
        self.last_refresh = datetime.datetime.now()

    def get_chart_data(self):
        price_list = []
        timestamp_list = []
        data = PriceData.objects.filter(stock=self.pk)
        data = data.order_by('time')
        for datum in data:
            price_list.append(datum.price)
            timestamp_list.append(datum.iso_time)
        return price_list, timestamp_list



class WatchList(models.Model):
    title = models.CharField(max_length=256)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    stocks = models.ManyToManyField(Stock)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def add_stock(self, stock):
        # Check if the stock is already in the watchlist
        if not self.stocks.filter(pk=stock.pk).exists():
            # Add the stock to the watchlist
            self.stocks.add(stock)
    def remove_stock(self, stock):
        if self.stocks.filter(pk=stock.pk).exists():
            # Add the stock to the watchlist
            self.stocks.remove(stock)

class PriceData(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    price = models.FloatField()
    time = models.DateTimeField()

    @classmethod
    def add(cls, stock, price, time):
        # Check if there is already an entry with the given symbol and time
        existing_entry = cls.objects.filter(stock=stock, time=time).first()
        if not existing_entry:
            # If entry does not exist, create a new one
            new_entry = cls(stock=stock, price=price, time=time)
            new_entry.save()

    @property
    def iso_time(self):
        py_time = datetime.datetime.strptime(self.time.__str__(), "%Y-%m-%d %H:%M:%S%z")
        return py_time.replace(tzinfo=None).isoformat()
