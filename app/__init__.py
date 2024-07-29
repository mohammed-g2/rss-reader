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
            values = {
                'name': 'Entrepreneur',
                'url': 'https://www.entrepreneur.com/latest.rss',
                'template': 'en.html',
                'title': 'title',
                'description': 'description',
                'items': {
                    '_id': 'item',
                    'title': 'title',
                    'link': 'link',
                    'published': 'pubDate',
                    'description': 'description'
                }
            }
        elif rss_feed == 'hbr':
            values = {
                'name': 'Harvard Business Review',
                'url': 'http://feeds.hbr.org/harvardbusiness/',
                'template': 'hbr.html',
                'title': 'title',
                'description': 'subtitle',
                'items': {
                    '_id': 'entry',
                    'title': 'title',
                    'link': 'link["href"]',
                    'published': 'published',
                    'description': 'summary'
                }
            }
        elif rss_feed == 'yahoo':
            values = {
                'name': 'Yahoo Finance',
                'url': 'https://finance.yahoo.com/rss/',
                'template': 'yahoo.html',
                'title': 'title',
                'description': 'description',
                'items': {
                    '_id': 'item',
                    'title': 'title',
                    'link': 'link',
                    'published': 'pubDate',
                    'description': None
                }
            }
        
        page = urlopen(values['url'])
        xml = page.read().decode('utf-8')
        soup = BeautifulSoup(markup=xml, features='xml')
        
        return render_template(
            'rss_feed.html',
            name=values['name'],
            title=getattr(soup, values['title']).string,
            description=getattr(soup, values['description']).string,
            items=soup.find_all(values['items']['_id']),
            item_tags=values['items'])

    return app
