from django.shortcuts import render
from .scraping import news_rss
from .weather import read_weather


def main(request):
    weather = read_weather()
    news = news_rss()
    return render(request, 'additional_app/index.html', {'weather': weather, 'news': news})