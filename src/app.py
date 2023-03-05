from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import DevConfig

app = Flask(__name__)
app.config.from_object(DevConfig)
db = SQLAlchemy(app)

@app.route('/')
def index():
    return "Hello World!"

class User(db.Model):
    id = db.Column(db.Integer(), primary_key = True)
    username = db.Column(db.String(255))
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
    
class Post(db.Model):
    id = db.Column(db.Integer(), primary_key = True)
    title = db.Column(db.String(255))
    text = db.Column(db.Text())
    publish_date = db.Column(db.DateTime())
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    comments = db.relationship(
        'Comment',
        backref = 'post',
        lazy = 'dynamic'
    )

    def __init__(self, title):
        self.title = title

    def __repr__(self):
        return f"<Post '{self.title}'>"

class Comment(db.Model):
    id = db.Column(db.Integer(), primary_key = True)
    name = db.Column(db.String(255))
    text = db.Column(db.Text())
    date = db.Column(db.DateTime())
    post_id = db.Column(db.Integer(), db.ForeignKey('post.id'))
    def __repr__(self):
        return "<Comment '{}'>".format(self.text[:15])

    def __repr__(self):
        return "<Comment '{}'>".format(self.text[:15])

if __name__ == '__main__':
    app.run()