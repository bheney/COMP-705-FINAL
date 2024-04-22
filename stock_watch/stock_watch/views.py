from django.views.generic.base import TemplateView


class Home(TemplateView):
    template_name = 'stock_watch/home.html'
