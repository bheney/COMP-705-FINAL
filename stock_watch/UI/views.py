from django.shortcuts import render
from .models import User, WatchList, Stock
# Create your views here.

def user_watchlists(request):
    # Assuming you have a way to identify the logged-in user, for example using Django's authentication system
    user = User.objects.get(id=request.user.id)
    
    # Retrieve the user's watchlists
    watchlists = Watchlist.objects.filter(user=user)
    
    # Iterate over each watchlist to get the stocks
    for watchlist in watchlists:
        watchlist.stocks = Stock.objects.filter(watchlist=watchlist)
    
    return render(request, 'watchlist.html', {'user': user, 'watchlists': watchlists})
