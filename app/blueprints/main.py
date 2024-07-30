from urllib.request import urlopen
from bs4 import BeautifulSoup
from flask import Blueprint, render_template, redirect, url_for, flash
from app import db
from app.models import Feed
from .forms import NewFeedForm

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    feeds = Feed.query.all()
    return render_template('index.html', feeds=feeds) 


@main_bp.route('/add-feed', methods=['GET', 'POST'])
def add_feed():
    form = NewFeedForm()
    if form.validate_on_submit():
        feed = Feed()
        feed.name = form.name.data
        feed.url = form.url.data
        feed.title_tag = form.title_tag.data
        feed.desc_tag = form.desc_tag.data
        feed.item_tag = form.item_tag.data
        feed.item_title_tag = form.item_title_tag.data
        feed.item_link_tag = form.item_link_tag.data
        feed.item_link_use_href = form.item_link_use_href.data
        feed.item_published_tag = form.item_published_tag.data
        feed.item_desc_tag = form.item_desc_tag.data
        
        db.session.add(feed)
        db.session.commit()
        flash('new feed added')
        return redirect(url_for('main.index'))
    
    return render_template('add-feed.html', form=form)


@main_bp.route('/feed/<int:id>')
def feed(id):
    feed = Feed.query.get_or_404(id)
    page = urlopen(feed.url)
    xml = page.read().decode('utf-8')
    soup = BeautifulSoup(markup=xml, features='xml')
    items = soup.find_all(feed.item_tag)
    _items = []

    for item in items:
        if feed.item_desc_tag:
            desc = getattr(item, feed.item_desc_tag).string
        else:
            desc = None
        
        if feed.item_link_use_href:
            link = getattr(item, feed.item_link_tag)['href']
        else:
            link = getattr(item, feed.item_link_tag).string
        
        _items.append({
            'id': feed.id,
            'title': getattr(item, feed.item_title_tag).string,
            'published': getattr(item, feed.item_published_tag).string,
            'description': desc,
            'link': link})
    
    return render_template(
        'rss-feed.html',
        name=getattr(soup, feed.title_tag).string,
        description=getattr(soup, feed.desc_tag).string,
        items=_items)
