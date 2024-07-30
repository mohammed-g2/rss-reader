from app import db


class FeedItem(db.Model):
    __tablename__ = 'feed_items'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), unique=True)
    published = db.Column(db.String())
    desc = db.Column(db.Text())
    link = db.Column(db.String())
    feed_id = db.Column(db.Integer, db.ForeignKey('feeds.id'))

    def __repr__(self):
        return f'<FeedItem {self.title}>'
