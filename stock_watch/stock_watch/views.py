from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView

from stock_watch.models import WatchList


class Home(TemplateView):
    template_name = 'stock_watch/home.html'


class WatchListEdit(DetailView):
    model = WatchList

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        watchlist = self.object  # Retrieve the WatchList object
        stocks = watchlist.stocks.all()  # Retrieve all related stocks
        context['stocks'] = stocks  # Add stocks to the context
        return context


