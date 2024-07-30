from threading import Thread
from urllib.request import urlopen
from bs4 import BeautifulSoup
from flask import current_app
from app import db
from app.models import FeedMap, Feed, FeedItem


def _scrap(feed_map):
    page = urlopen(feed_map.url)
    xml = page.read().decode('utf-8')
    soup = BeautifulSoup(markup=xml, features='xml')
    items = soup.find_all(feed_map.item_tag)

    feed = Feed.query.filter_by(
        name=getattr(soup, feed_map.title_tag).string).first()
    if not feed:
        feed = Feed()
        feed.name = getattr(soup, feed_map.title_tag).string
        feed.desc = getattr(soup, feed_map.desc_tag).string
        db.session.add(feed)
        db.session.commit()

    for item in items:
        feed_item = FeedItem.query.filter_by(
            title=getattr(item, feed_map.item_title_tag).string).first()
        if not feed_item:
            feed_item = FeedItem()
            if feed_map.item_desc_tag:
                desc = getattr(item, feed_map.item_desc_tag).string
            else:
                desc = None
            
            if feed_map.item_link_use_href:
                link = getattr(item, feed_map.item_link_tag)['href']
            else:
                link = getattr(item, feed_map.item_link_tag).string
            
            feed_item.title = getattr(item, feed_map.item_title_tag).string
            feed_item.published = getattr(item, feed_map.item_published_tag).string
            feed_item.desc = desc
            feed_item.link = link
            feed_item.feed = feed

            db.session.add(feed_item)
    db.session.commit()


def _timed_scrap(app):
    with app.app_context():
        print('Running timed job, Scraping')
        for feed_map in FeedMap.query.all():
            _scrap(feed_map)


def _async_scrap(app, feed_map):
    with app.app_context():
        _scrap(feed_map)


def scrap(feed_map: FeedMap):
    thr = Thread(
        target=_async_scrap, 
        args=[current_app._get_current_object(), feed_map])
    thr.start()
    return thr
