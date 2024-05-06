from django.views import View
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse

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

class WatchlistRemoveEntry(View):
    template_name = 'stock_watch/watchlist_remove_entry.html'
    success_url = reverse_lazy('close_popup')

    def get(self, request, watchlist_pk, stock_pk):
        # Retrieve the watchlist and stock objects
        watchlist = WatchList.objects.get(pk=watchlist_pk)
        stock = Stock.objects.get(pk=stock_pk)

        # Render the confirmation page with context
        return render(request, self.template_name, {'stock': stock, 'list': watchlist})

class WatchListAPI(View):
    @staticmethod
    def remove_stock(request):
        # Get the watchlist_id and stock_id from the query parameters
        watchlist_id = request.GET.get('watchlist_id')
        stock_id = request.GET.get('stock_id')

        # Perform any necessary validation or processing
        if watchlist_id is None or stock_id is None:
            # Handle missing parameters
            return redirect('error_page')

        # Retrieve the watchlist and stock objects
        watchlist = get_object_or_404(WatchList, pk=watchlist_id)
        stock = get_object_or_404(Stock, pk=stock_id)

        # Perform the remove action
        watchlist.stocks.remove(stock)

        # Redirect to a success URL (e.g., a page showing the updated watchlist)
        return redirect('watchlist_detail', pk=watchlist_id)




class StockView(DetailView):
    model = Stock

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        stock = self.object  # Retrieve the Stock object
        stock.update()  # TODO: This needs to be handled by a backend thread
        price_list, timestamp_list = stock.get_chart_data()
        context['price_list'] = price_list
        context['timestamp_list'] = timestamp_list
        return context

def close_popup(request):
    return HttpResponse()
