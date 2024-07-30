import os
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv
from app import create_app, db
from app.models import FeedMap, Feed, FeedItem
from app.util import scrap, _timed_scrap
from config import basedir

load_dotenv(os.path.join(basedir, '.env'))

app = create_app(os.environ.get('APP_CONFIG', 'default'))

schedular = BackgroundScheduler(daemon=True)
schedular.add_job(func=_timed_scrap, trigger='interval', args=[app], hours=24)
schedular.start()
atexit.register(lambda: schedular.shutdown(wait=False))


@app.cli.command('init')
def init():
    """initialize the application"""
    tmp_dir = os.path.join(basedir, 'tmp')
    dev_db_dir = os.path.join(tmp_dir, 'dev-data.sqlite')
    if not os.path.exists(tmp_dir):
        os.makedirs(tmp_dir)
        print('Created folder for temporary files.')
    if os.path.exists(dev_db_dir):
        db.drop_all()
        print('Dropped database')
    db.create_all()
    print('Created database.')


@app.cli.command('scrap')
def scrap_rss_feeds():
    """Scrap all rss feeds stored in database"""
    for feed in FeedMap.query.all():
        scrap(feed)
        print(f'Got: {feed.name} @{feed.url}')


@app.shell_context_processor
def shell_context():
    return dict(db=db, FeedMap=FeedMap, Feed=Feed, FeedItem=FeedItem)


@app.context_processor
def template_context():
    return dict()
