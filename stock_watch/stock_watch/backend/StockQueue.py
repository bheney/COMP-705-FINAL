import datetime
import time
from stock_watch.models import WatchList

from django.conf import settings


class StockQueue:

    def __init__(self):
        self.queue = []
        self.run = False
        self.last_update = None

    def add(self, stock):
        if stock not in self.queue:
            self.queue.append(stock)

    def open_monitor(self):
        self.run = True
        while self.run:
            while self.run & self.trading_is_open():
                head = self.queue.pop()
                self.queue.append(head)
                head.update()
                self.last_update = datetime.datetime.now()
                self.prune()
                time.sleep(settings.REFRESH_INTERVAL)

    def close_monitor(self):
        self.run = False

    @staticmethod
    def trading_is_open():
        now = datetime.datetime.now().time()
        if settings.OPEN < settings.CLOSE:
            return settings.OPEN <= now <= settings.CLOSE
        return not (settings.CLOSE < now < settings.OPEN)

    def prune(self):
        watchlists = WatchList.objects.all()
        for watchlist in watchlists:
            for stock in self.queue:
                if not watchlist.stocks.filter(pk=stock.pk).exists():
                    self.queue.remove(stock)

    def get_next_update(self, stock):
        index = self.queue.index(stock)
        sec_to_next_update = settings.REFRESH_INTERVAL * (index + 1)
        return self.last_update + datetime.timedelta(seconds=sec_to_next_update)

