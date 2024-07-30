from app import db


class FeedMap(db.Model):
    __tablename__ = 'feed_maps'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), index=True, unique=True)
    url = db.Column(db.String(), index=True, unique=True)
    title_tag = db.Column(db.String())
    desc_tag = db.Column(db.String())
    item_tag = db.Column(db.String())
    item_title_tag = db.Column(db.String())
    item_link_tag = db.Column(db.String())
    item_link_use_href = db.Column(db.Boolean())
    item_published_tag = db.Column(db.String())
    item_desc_tag = db.Column(db.String())

    def __repr__(self):
        return f'<FeedMap {self.name}>'
