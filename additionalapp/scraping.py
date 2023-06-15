from calendar import prcal

import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import lxml


def news_rss():
    article_list = []
    id = 0
    source_neus = {
        #'https://www.rbc.ua/static/rss/all.ukr.rss.xml': 'РБК-Украина',
        'https://www.radiosvoboda.org/api/zrqiteuuir': 'Радіо Свобода',
        #'https://www.unn.com.ua/rss/news_uk.xml': 'Українські Національні Новини (УНН)',
        #'https://www.pravda.com.ua/rss/view_news/': 'Українська правда',
        'https://nv.ua/ukr/rss/all.xml': 'Новини NV',

    }
    try:
        print('Starting the scraping tool')
        for source_n, source_name in source_neus.items():
            print(f"Start: {source_name}")
            r = requests.get(source_n)
            soup = BeautifulSoup(r.content, features='xml')
            articles = soup.findAll('item')
            for a in articles:
                title = a.find('title').text
                link = a.find('link').text
                description = a.find('description').text
                published_wrong = datetime.strptime(a.find('pubDate').text, '%a, %d %b %Y %H:%M:%S %z')
                published = published_wrong.strftime('%H:%M - %d.%m.%Y')
                img = a.enclosure['url']

                article = {
                    'id': id,
                    'title': title,
                    'link': link,
                    'description': description,
                    'published': published,
                    'img': img,
                    'source': source_name
                }
                article_list.append(article)
                id += id
            print(f"Completed scraping: {source_name}")
        print('Finished scraping the articles')
        article_list = sorted(article_list, key=lambda x: datetime.strptime(x['published'], '%H:%M - %d.%m.%Y'), reverse=True)
        return article_list
    except Exception as error:
        print('The scraping job failed. See exception:')
        print(error)