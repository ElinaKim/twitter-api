from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from config import DevConfig
import datetime
from flask_migrate import Migrate
from sqlalchemy import func

app = Flask(__name__)
app.config.from_object(DevConfig)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

@app.route('/')
def index():
    return "Hello World!"



class User(db.Model):
    id = db.Column(db.Integer(), primary_key = True)
    username = db.Column(db.String(255), nullable = False, unique = True)
    password = db.Column(db.String(255))
    posts = db.relationship (
        'Post',
        backref = 'user', 
        lazy = 'dynamic'
    )

    def __init__(self, username):
        self.username = username
    
    def __repr__(self):
        return f"User '{self.username}'"

#used to establish many-to-many relationship between posts and tags
tags = db.Table('post_tags', db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
                db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')))
    
class Post(db.Model):
    id = db.Column(db.Integer(), primary_key = True)
    title = db.Column(db.String(255), nullable = False)
    text = db.Column(db.Text())
    publish_date = db.Column(db.DateTime(), default = datetime.datetime.now)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    comments = db.relationship(
        'Comment',
        backref = 'post',
        lazy = 'dynamic'
    )
    tags = db.relationship(
        'Tag',
        secondary = tags, 
        backref = db.backref('posts', lazy = 'dynamic')
    )

    def __init__(self, title):
        self.title = title

    def __repr__(self):
        return f"<Post '{self.title}'>"

class Tag(db.Model):
    id = db.Column(db.Integer(), primary_key = True)
    title = db.Column(db.String(255), nullable = False, unique = True)
    
    def __init__(self, title):
        self.title = title
    
    def __repr__(self):
        return "<Tag>'{}'>".format(self.title)

class Comment(db.Model):
    id = db.Column(db.Integer(), primary_key = True)
    name = db.Column(db.String(255), nullable = False)
    text = db.Column(db.Text())
    date = db.Column(db.DateTime(), default = datetime.datetime.now)
    post_id = db.Column(db.Integer(), db.ForeignKey('post.id'))
    def __repr__(self):
        return "<Comment '{}'>".format(self.text[:15])

    def __repr__(self):
        return "<Comment '{}'>".format(self.text[:15])

def sidebar_data():
    recent = Post.query.order_by(
        Post.publish_date.desc()
    ).limit(5).all()
    top_tags = db.session.query(
        Tag, func.count(tags.c.post_id).label('total')
    ).join(
        tags
    ).group_by(Tag).order_by('total DESC').limit(5).all()

    return recent, top_tags



if __name__ == '__main__':
    app.run()