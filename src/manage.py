from app import app, db, User, Post, Comment, Tag, tags, migrate 

@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db, User=User, Post=Post, Comment=Comment, Tag=Tag, post_tags=tags, migrate=migrate)