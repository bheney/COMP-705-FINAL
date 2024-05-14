# forms.py
from django import forms
from django.utils import timezone

from stock_watch.models import Stock, WatchList


class AddNewStockToWatchlist(forms.Form):
    stock = forms.ModelChoiceField(
        queryset=Stock.objects.none(),
        empty_label='Select a stock',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['stock'].queryset = Stock.objects.all().order_by('symbol')
        self.fields['stock'].label = 'Stock Symbol'


class AddNewWatchList(forms.Form):
    title = forms.CharField(label="Title", max_length=64)
    stocks = forms.ModelMultipleChoiceField(queryset=Stock.objects.all().order_by('symbol'))

    def __init__(self, user_instance, *args, **kwargs):
        del kwargs['instance']
        super(AddNewWatchList, self).__init__(*args, **kwargs)
        self.user_instance = user_instance

    def save(self):
        watchlist = WatchList.objects.create(
            title=self.cleaned_data['title'],
            user_id=self.user_instance,
            created_at=timezone.now(),
            updated_at=timezone.now()
        )
        watchlist.stocks.set(self.cleaned_data['stocks'])
        return watchlist