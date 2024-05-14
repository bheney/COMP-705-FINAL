# forms.py
from django import forms

from stock_watch.models import Stock


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
    stock = forms.ModelChoiceField(
        queryset=Stock.objects.none(),
        empty_label='Select a stock',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['stock'].queryset = Stock.objects.all().order_by('symbol')
        self.fields['stock'].label = 'Stock Symbol'