from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView

from stock_watch.models import WatchList, Stock
from django.shortcuts import render
from django.conf import settings

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
        stock = self.object  # Retrieve the WatchList object
        return context

def index(request):
    return render(request, 'index.html', {'TWELVE_DATA_API_KEY': settings.TWELVE_DATA_API_KEY})
