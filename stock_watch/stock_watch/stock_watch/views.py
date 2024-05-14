import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.views import View
from django.views.generic import ListView
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView

from django.urls import reverse_lazy
from django.http import HttpResponse, JsonResponse

from stock_watch.models import WatchList, Stock
from stock_watch.forms import AddNewStockToWatchlist, AddNewWatchList
from stock_watch.serializers import WatchListSerializer

from django.shortcuts import render
from django.conf import settings

class Home(TemplateView):
    template_name = 'stock_watch/home.html'


class WatchListView(DetailView):
    model = WatchList
    template_name = 'stock_watch/watchlist_detail.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        watchlist = self.object  # Retrieve the WatchList object
        stocks = watchlist.stocks.all()  # Retrieve all related stocks
        context['stocks'] = stocks  # Add stocks to the context
        return context

class UserWatchListsView(DetailView):
    model = User
    template_name = 'stock_watch/manage_watch_lists.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        watchlists = WatchList.objects.filter(user_id=self.object.pk)  # Retrieve the WatchList object
        context['watchlists'] = watchlists
        context['user'] = self.object
        return context


class RemoveWatchList(View):
    template_name = 'stock_watch/remove_watchlist.html'
    success_url = reverse_lazy('close_popup')

class AddWatchList(CreateView):
    model = WatchList
    form_class = AddNewWatchList
    template_name = 'stock_watch/add_watchlist.html'
    success_url = reverse_lazy('close_popup')

class WatchlistRemoveEntry(View):
    template_name = 'stock_watch/watchlist_remove_entry.html'
    success_url = reverse_lazy('close_popup')

    def get(self, request, watchlist_pk, stock_pk):
        # Retrieve the watchlist and stock objects
        watchlist = WatchList.objects.get(pk=watchlist_pk)
        stock = Stock.objects.get(pk=stock_pk)

        # Render the confirmation page with context
        return render(request, self.template_name, {'stock': stock, 'list': watchlist})

class WatchlistAddEntry(View):
    template_name = "stock_watch/watchlist_add_entry.html"

    def get(self, request, watchlist_pk):
        # TODO: Handle arguments with Args and kwargs
        form = AddNewStockToWatchlist()
        return render(request, self.template_name, {'form': form, 'list': watchlist_pk})
    def post(self, request, watchlist_pk):
        # TODO: Handle arguments with Args and kwargs
        form = AddNewStockToWatchlist(request.POST)
        if form.is_valid():
            symbol = form.cleaned_data['symbol']
            # Call the API class to process the search
            result = WatchListAPI.AddStockToWatchlist(symbol)
            return JsonResponse({'success': True, 'result': result})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})

class WatchListAPI:
    class RemoveStockFromWatchlist(View):
        def post(self, request):
            try:
                # Retrieve the watchlist and stock objects
                watchlist = WatchList.objects.get(pk=request.GET.get('list'))
                stock = Stock.objects.get(pk=request.GET.get('stock'))

                # Remove the stock from the watchlist
                watchlist.stocks.remove(stock)
                watchlist.updated_at = datetime.datetime.now()
                watchlist.save()

                # Return a success JSON response
                return JsonResponse({'success': True})
            except Exception as e:
                # Return an error JSON response
                return JsonResponse({'success': False, 'error': str(e)})

    class AddStockToWatchlist(View):
        def post(self, request):
            # try:
                # Retrieve the watchlist and stock objects
                watchlist = WatchList.objects.get(pk=request.GET.get('list'))
                stock = Stock.objects.get(pk=request.GET.get('stock'))

                # Add the stock from the watchlist
                if stock not in watchlist.stocks.all():
                    watchlist.stocks.add(stock)
                    watchlist.updated_at = datetime.datetime.now()
                    watchlist.save()

                # Return a success JSON response
                return JsonResponse({'success': True})
                '''
                except Exception as e:
                    # Return an error JSON response
                    return JsonResponse({'success': False, 'error': str(e)})
                '''

    class RemoveWatchlist(View):
        def post(self, request):
            watchlist=WatchList.objects.get(pk=request.GET.get('list'))

            if not request.user.is_authenticated:
                return HttpResponse(status_code=401)
            if request.user.pk != watchlist.user_id:
                return HttpResponse(status_code=401)

            watchlist.delete()
            return HttpResponse(status_code=200)
    class AddWatchlist(View):
        def post(self, request):
            serializer = WatchListSerializer(data=request.data)

            if not request.user.is_authenticated:
                return HttpResponse(status_code=401)
            if serializer.is_valid():
                serializer.save()
                return HttpResponse(status_code=201)
            return HttpResponse(status_code=400)


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

def index(request):
    return render(request, 'index.html', {'TWELVE_DATA_API_KEY': settings.TWELVE_DATA_API_KEY})


def close_popup(request):
    return HttpResponse()
