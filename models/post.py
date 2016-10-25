from google.appengine.ext import db
from models.user import User


class Post(db.Model):
    subject = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    author = db.ReferenceProperty(User, collection_name='posts_collection', required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    last_modified = db.DateTimeProperty(auto_now = True)

    @classmethod
    def by_id(cls, post_id):
        return cls.get_by_id(int(post_id),parent = cls.blog_key())

    
    @classmethod
    def blog_key(cls, name = 'default'):
        return db.Key.from_path('blogs', name)

    def like_by(self, like, user):
        if user.username == self.author.username or not self.likes_collection:
            return None
        likes = self.likes_collection;
        l = [x for x in likes if x.user.username == user.username]
        if not like:
            for x in l:
                x.delete()
            return None
        else:
            return l or Like.like(user, self)

    def is_liked_by(self, user):
        if not self.likes_collection:
            return None
        likes = self.likes_collection;
        l = [like for like in likes if like.user.username == user.username]
        return l


class Like(db.Model):
    user = db.ReferenceProperty(User, collection_name='likes_collection', required = True)
    post = db.ReferenceProperty(Post, collection_name='likes_collection', required = True)

    @classmethod
    def by_id(cls, post_id):
        return cls.get_by_id(int(post_id))

    @classmethod
    def like(cls,user, post):
        return Like(user=user, post=post, parent=cls.like_key()).put()
    
    @classmethod
    def like_key(cls, name = 'default'):
        return db.Key.from_path('likes', name)
