from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView

from stock_watch.models import WatchList, Stock


class Home(TemplateView):
    template_name = 'stock_watch/home.html'


class WatchListView(DetailView):
    model = WatchList

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        watchlist = self.object  # Retrieve the WatchList object
        stocks = watchlist.stocks.all()  # Retrieve all related stocks
        context['stocks'] = stocks  # Add stocks to the context
        return context


class StockView(DetailView):
    model = Stock

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        stock = self.object  # Retrieve the Stock object
        stock.update() # TODO: This needs to be handled by a backend thread
        price_list, timestamp_list = stock.get_chart_data()
        context['price_list'] = price_list
        context['timestamp_list'] = timestamp_list
        return context
