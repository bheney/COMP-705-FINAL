from django.shortcuts import render
from .models import User, WatchList, Stock
import requests
from django.http import JsonResponse
# Create your views here.

def home(request):
    return render(request, 'home.html', {})

def get_ticker(request):
    # URL to fetch data from
    ticker = request.GET.get('ticker', '')

    url = f"https://api.twelvedata.com/stocks?symbol={ticker}&apikey=1f26dee0a04840be8b136374ebb2ad79"

    print(url)

    # Make a GET request to the URL
    response = requests.get(url)
    
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Return the JSON response from the API
        return JsonResponse(response.json())
    else:
        # If the request was not successful, return an error response
        return JsonResponse({"error": "Failed to fetch data"}, status=500)

def user_watchlists(request):
    # Assuming you have a way to identify the logged-in user, for example using Django's authentication system
    user = User.objects.get(id=request.user.id)
    
    # Retrieve the user's watchlists
    watchlists = Watchlist.objects.filter(user=user)
    
    # Iterate over each watchlist to get the stocks
    for watchlist in watchlists:
        watchlist.stocks = Stock.objects.filter(watchlist=watchlist)
    
    return render(request, 'watchlist.html', {'user': user, 'watchlists': watchlists})
