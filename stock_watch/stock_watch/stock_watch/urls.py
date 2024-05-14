"""
URL configuration for stock_watch project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
import stock_watch.views as views

urlpatterns = [
    # Page Views
    path('admin/', admin.site.urls),
    path(route='', view=views.Home.as_view(), name='home'),
    path('watchlist/<int:pk>/', views.WatchListView.as_view(), name='watchlist_edit'),
    path('stock/<int:pk>/', views.StockView.as_view(), name='stock_detail'),
    path('confirm_stock_delete/<int:watchlist_pk>/<int:stock_pk>', views.WatchlistRemoveEntry.as_view(), name='confirm_remove_stock'),
    path('add_new_stock/<int:watchlist_pk>', views.WatchlistAddEntry.as_view() ,name='add_new_stock'),
    path('close_popup/', views.close_popup, name='close_popup'),
    path('watchlists/<int:pk>', views.UserWatchListsView.as_view(), name='user_watchlist_list'),
    path('confirm_remove_watchlist/<int:pk>', views.RemoveWatchList.as_view(), name='confirm_remove_watchlist'),
    path('add_watchlist/', views.AddWatchList.as_view(), name='add_new_watchlist'),

    # Internal API
    path('api/remove_stock/', views.WatchListAPI.RemoveStockFromWatchlist.as_view(), name='remove_stock'),
    path('api/add_stock/', views.WatchListAPI.AddStockToWatchlist.as_view(), name='add_stock'),
    path('api/delete_watchlist/', views.WatchListAPI.RemoveWatchlist.as_view(), name='remove_watchlist'),
    path('api/add_watchlist/', views.WatchListAPI.AddWatchlist.as_view(), name='add_watchlist'),
]

