from urllib.request import urlopen
from bs4 import BeautifulSoup
from flask import Flask, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from config import options


db = SQLAlchemy()


def create_app(config_name: str) -> Flask:
    """Create and configure the application"""
    app = Flask(__name__)
    app.config.from_object(options[config_name])

    db.init_app(app)
    
    from app.blueprints import main_bp
    app.register_blueprint(main_bp)

    return app
