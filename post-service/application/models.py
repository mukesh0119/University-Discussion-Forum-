# application/models.py
from . import db
from datetime import datetime

class Post(db.Model):
    __searchable__ = ['title','content']
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    user_name = db.Column(db.String(255), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(20), index=True, nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.Text,nullable=True)
    comments = db.relationship('Comment', backref='post', lazy='dynamic')

    def __repr__(self):
        return '<Post %r>' % (self.title + str(self.id))

    def to_json(self):
        return {
        'id': self.id,
        'user_id': self.user_id,
        'user_name':self.user_name,
        'title': self.title,
        'category': self.category,
        'date_added': self.date_added,
        'content' : self.content,
        'image_url':self.image_url
    }


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    disabled = db.Column(db.Boolean)
    user_id = db.Column(db.Integer)
    user_name = db.Column(db.String(255), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))

    def __repr__(self):
        return '<Comment %r>' % (str(self.post_id) + '-' + str(self.id))

    def to_json(self):
        return {
        'id': self.id,
        'post_id': self.post_id,
        'user_id': self.user_id,
        'user_name': self.user_name,
        'content': self.content,
        'date_added': self.date_added
    }
