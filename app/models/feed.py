from app import db


class Feed(db.Model):
    __tablename__ = 'feeds'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), index=True)
    url = db.Column(db.String())
    title_tag = db.Column(db.String())
    desc_tag = db.Column(db.String())
    item_tag = db.Column(db.String())
    item_title_tag = db.Column(db.String())
    item_link_tag = db.Column(db.String())
    item_link_use_href = db.Column(db.Boolean())
    item_published_tag = db.Column(db.String())
    item_desc_tag = db.Column(db.String())

    def __repr__(self):
        return f'<Feed {self.name}>'
