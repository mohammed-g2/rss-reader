from app import db


class Feed(db.Model):
    __tablename__ = 'feeds'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), index=True, unique=True)
    desc = db.Column(db.String())
    items = db.relationship('FeedItem', backref='feed', lazy='dynamic')

    def __repr__(self):
        return f'<Feed {self.name}>'
