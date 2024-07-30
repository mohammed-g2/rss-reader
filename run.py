import os
from dotenv import load_dotenv
from app import create_app, db
from app.models import Feed
from config import options, basedir

load_dotenv(os.path.join(basedir, '.env'))

app = create_app(os.environ.get('APP_CONFIG', 'default'))


@app.cli.command('init')
def init():
    """initialize the application"""
    tmp_dir = os.path.join(basedir, 'tmp')
    if not os.path.exists(tmp_dir):
        os.makedirs(tmp_dir)
        print('Created folder for temporary files.')
    db.create_all()
    print('Created database.')


@app.shell_context_processor
def shell_context():
    return dict(db=db, Feed=Feed)


@app.context_processor
def template_context():
    return dict()
