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
<<<<<<< HEAD:stock_watch/stock_watch/urls.py
from django.urls import path
from . import views
from .views import WatchListView, StockView

urlpatterns = [
    path('admin/', admin.site.urls),
    path(route='', view=views.Home.as_view(), name='home'),
    path('watchlist/<int:pk>/', WatchListView.as_view(), name='watchlist_edit'),
    path('stock/<int:pk>/', StockView.as_view(), name='watchlist_edit'),
=======
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("UI.urls")),
    
>>>>>>> 0044a93dd79861078ca51f4ad29a50e6ced7ffed:stock_watch/urls.py
]

