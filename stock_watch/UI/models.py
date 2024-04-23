# models.py

from django.db import models

class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

class WatchList(models.Model):
    title = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    stocks = models.ManyToManyField('Stock', through='WatchListStocks', related_name='watchlists')

class Stock(models.Model):
    symbol = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=255)
    market = models.CharField(max_length=100)
    next_refresh = models.TimeField()

class WatchListStocks(models.Model):
    watchlist = models.ForeignKey(WatchList, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)

    class Meta:
        db_table = 'UI_watchliststocks'
        unique_together = ('watchlist', 'stock')
