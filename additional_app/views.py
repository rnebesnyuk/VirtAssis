from django.shortcuts import render
from .scraping import news_rss
from .weather import read_weather
from .utils import DataMixin, menu, apps


def main(request):
    weather = read_weather()
    news = news_rss()
    title = "Home"
    return render(request, 'additional_app/index.html', {'weather': weather, 'news': news, 'title': title, 'menu': menu, 'apps': apps})