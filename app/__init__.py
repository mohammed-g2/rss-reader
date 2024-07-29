from urllib.request import urlopen
from bs4 import BeautifulSoup
from flask import Flask, render_template, url_for, redirect
from config import options


def create_app(config_name: str) -> Flask:
    """Create and configure the application"""
    app = Flask(__name__)
    app.config.from_object(options[config_name])

    @app.route('/')
    def index():
        return render_template('index.html')


    @app.route('/<rss_feed>')
    def feed(rss_feed):
        accepted_rss_feeds = ['entrepreneur', 'hbr', 'yahoo']
        if rss_feed not in accepted_rss_feeds:
            return redirect(url_for('index'))
        
        if rss_feed == 'entrepreneur':
            map = {
                'name': 'Entrepreneur',
                'url': 'https://www.entrepreneur.com/latest.rss',
                'template': 'en.html',
                'title': 'title',
                'description': 'description',
                'items': {
                    '_id': 'item',
                    'title': 'title',
                    'link': {'name': 'link', 'attr': False},
                    'published': 'pubDate',
                    'description': 'description'
                }
            }
        elif rss_feed == 'hbr':
            map = {
                'name': 'Harvard Business Review',
                'url': 'http://feeds.hbr.org/harvardbusiness/',
                'template': 'hbr.html',
                'title': 'title',
                'description': 'subtitle',
                'items': {
                    '_id': 'entry',
                    'title': 'title',
                    'link': {'name': 'link', 'attr': 'href'},
                    'published': 'published',
                    'description': 'summary'
                }
            }
        elif rss_feed == 'yahoo':
            map = {
                'name': 'Yahoo Finance',
                'url': 'https://finance.yahoo.com/rss/',
                'template': 'yahoo.html',
                'title': 'title',
                'description': 'description',
                'items': {
                    '_id': 'item',
                    'title': 'title',
                    'link': {'name': 'link', 'attr': False},
                    'published': 'pubDate',
                    'description': None
                }
            }
        
        page = urlopen(map['url'])
        xml = page.read().decode('utf-8')
        soup = BeautifulSoup(markup=xml, features='xml')
        items = soup.find_all(map['items']['_id'])

        def set_items(items, map):
            _items = []
            for item in items:
                if map['description'] is not None:
                    desc = getattr(item, map['description']).string
                else:
                    desc = None
                
                if map['link']['attr'] is not False:
                    link = getattr(item, map['link']['name'])[map['link']['attr']]
                else:
                    link = getattr(item, map['link']['name']).string
                
                _items.append({
                    '_id': map['_id'],
                    'title': getattr(item, map['title']).string,
                    'published': getattr(item, map['published']).string,
                    'description': desc,
                    'link': link})
            return _items

        return render_template(
            'rss_feed.html',
            name=map['name'],
            title=getattr(soup, map['title']).string,
            description=getattr(soup, map['description']).string,
            items=set_items(items, map['items']))

    return app
