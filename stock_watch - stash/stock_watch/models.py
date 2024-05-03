from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


class Stock(models.Model):
    symbol = models.CharField(max_length=settings.MAX_SYMBOL_LENGTH)
    name = models.CharField()
    exchange = models.CharField()
    last_refresh = models.DateTimeField()

    def __eq__(self, other):
        if other is Stock:
            return self.symbol == other.symbol
        if other is str:
            return self.symbol == other
        raise TypeError("Equality for class Stock is only defined for other Stocks and strings")

    def update(self):
        pass
    # TODO: Make an API call and update the data


class WatchList(models.Model):
    title = models.CharField()
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    stocks = models.ManyToManyField(Stock)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
