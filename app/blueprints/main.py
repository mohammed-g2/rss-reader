from flask import Blueprint, render_template, redirect, url_for, flash, request
from app import db
from app.models import FeedMap, Feed
from app.util import scrap
from .forms import NewFeedForm, DeleteFeedForm

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    feeds = FeedMap.query.all()
    delete_feed_form = DeleteFeedForm()
    return render_template('index.html', feeds=feeds, delete_feed_form=delete_feed_form) 


@main_bp.route('/feed/<int:id>')
def feed(id):
    feed = Feed.query.get_or_404(id)
    return render_template('rss-feed.html', feed=feed)


@main_bp.route('/add-feed', methods=['GET', 'POST'])
def add_feed():
    form = NewFeedForm()
    if form.validate_on_submit():
        feed_map = FeedMap()
        feed_map.name = form.name.data
        feed_map.url = form.url.data
        feed_map.title_tag = form.title_tag.data
        feed_map.desc_tag = form.desc_tag.data
        feed_map.item_tag = form.item_tag.data
        feed_map.item_title_tag = form.item_title_tag.data
        feed_map.item_link_tag = form.item_link_tag.data
        feed_map.item_link_use_href = form.item_link_use_href.data
        feed_map.item_published_tag = form.item_published_tag.data
        feed_map.item_desc_tag = form.item_desc_tag.data
        
        db.session.add(feed_map)
        db.session.commit()
        
        scrap(feed_map)
        flash('new feed added')
        return redirect(url_for('main.index'))

    return render_template('add-feed.html', form=form)


@main_bp.route('/edit-feed/<int:id>', methods=['GET', 'POST'])
def edit_feed(id):
    feed_map = FeedMap.query.get_or_404(id)
    form = NewFeedForm()
    if form.validate_on_submit():
        feed_map.name = form.name.data
        feed_map.url = form.url.data
        feed_map.title_tag = form.title_tag.data
        feed_map.desc_tag = form.desc_tag.data
        feed_map.item_tag = form.item_tag.data
        feed_map.item_title_tag = form.item_title_tag.data
        feed_map.item_link_tag = form.item_link_tag.data
        feed_map.item_link_use_href = form.item_link_use_href.data
        feed_map.item_published_tag = form.item_published_tag.data
        feed_map.item_desc_tag = form.item_desc_tag.data
        
        db.session.add(feed_map)
        db.session.commit()
        flash('feed updated')
        return redirect(url_for('main.index'))
    
    form.name.data = feed_map.name
    form.url.data = feed_map.url
    form.title_tag.data = feed_map.title_tag
    form.desc_tag.data = feed_map.desc_tag
    form.item_tag.data = feed_map.item_tag
    form.item_title_tag.data = feed_map.item_title_tag
    form.item_link_tag.data = feed_map.item_link_tag
    form.item_link_use_href.data = feed_map.item_link_use_href
    form.item_published_tag.data = feed_map.item_published_tag
    form.item_desc_tag.data = feed_map.item_desc_tag

    return render_template('add-feed.html', form=form)


@main_bp.route('/delete-feed', methods=['POST'])
def delete_feed():
    form = DeleteFeedForm(request.form)
    feed_map = FeedMap.query.get_or_404(form.id.data)
    if form.validate_on_submit():
        db.session.delete(feed_map)
        db.session.commit()
        flash('feed deleted')
    return redirect(url_for('main.index'))
