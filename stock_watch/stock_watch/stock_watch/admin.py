# Inside yourapp/admin.py

from django.contrib import admin
from .models import Stock, WatchList

admin.site.register(Stock)
admin.site.register(WatchList)
