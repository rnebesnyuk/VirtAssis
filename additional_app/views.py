from django.shortcuts import render

from .scraping import news_rss
from .weather import read_weather
from .exchange import exchange_list
from .utils import DataMixin, menu, apps


def main(request):
    city = ''
    if request.POST:
        city = request.POST.get("city", "Undefined")
    if not city:
        city = 'Kiev'
    print(f"Введене місто: {city}")
    weather = read_weather(city)
    exchange = exchange_list()
    news = news_rss()
    title = "Home"
    return render(request, 'additional_app/index.html', {'weather': weather, 'news': news, 'title': title, 'menu': menu, 'apps': apps, 'exchange': exchange})