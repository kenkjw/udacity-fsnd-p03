from google.appengine.ext import db
from models.user import User



class Comment(db.Model):
    subject = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    author = db.ReferenceProperty(User, collection_name='posts_collection', required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    last_modified = db.DateTimeProperty(auto_now = True)

    @classmethod
    def by_id(cls, post_id):
        return cls.get_by_id(int(post_id),parent = comment_key())

    @classmethod
    def comment_key(cls, name = 'default'):
        return db.Key.from_path('comments', name)