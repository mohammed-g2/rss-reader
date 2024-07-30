from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, HiddenField
from wtforms.validators import DataRequired, ValidationError
from app.models import FeedMap


class NewFeedForm(FlaskForm):
    name = StringField('Website Name', validators=[DataRequired()])
    url = StringField('RSS Feed URL', validators=[DataRequired()])
    title_tag = StringField('Title Tag', validators=[DataRequired()])
    desc_tag = StringField('Description Tag')
    item_tag = StringField('Item / Entry Tag', validators=[DataRequired()])
    item_title_tag = StringField('Item Title Tag', validators=[DataRequired()])
    item_link_tag = StringField('Item Link Tag', validators=[DataRequired()])
    item_link_use_href = BooleanField('Item Link Use href')
    item_published_tag = StringField('Item Published Date Tag')
    item_desc_tag = StringField('Item Description Tag')
    submit = SubmitField('Add Feed')

    def validate_name(self, field):
        if FeedMap.query.filter_by(name=field.data).first():
            raise ValidationError('Feed already registered')

    def validate_url(self, field):
        if FeedMap.query.filter_by(url=field.data).first():
            raise ValidationError('URL already registered')


class DeleteFeedForm(FlaskForm):
    id = HiddenField('id', validators=[DataRequired()])
    submit = SubmitField('Delete')
