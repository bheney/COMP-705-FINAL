from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("ticker", views.get_ticker, name="home")

]