import os
from dotenv import load_dotenv
from app import create_app
from config import options


app = create_app(os.environ.get('APP_CONFIG', 'default'))


@app.shell_context_processor
def shell_context():
    return dict()


@app.context_processor
def template_context():
    return dict()
