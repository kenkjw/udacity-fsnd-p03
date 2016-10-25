from google.appengine.ext import db

from models.user import User


class Post(db.Model):
    """ Google AppEngine Datastore Entity representing a single blog post.

    The class provides a few extra methods on top of the standard model class
    for getting/setting likes and comments.
    
    Properties:
        subject: A string representing the subject of the blog post.
        content: The textual content of the blog post.
        author: A reference to the user that created the post.
        created: DateTime representing the creation of the post.
        last_modified: DateTime representing the last modified time.

    """

    subject = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    author = db.ReferenceProperty(User, collection_name="posts_collection", 
                                  required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    last_modified = db.DateTimeProperty(auto_now=True)

    @classmethod
    def by_id(cls, post_id):
        return cls.get_by_id(int(post_id), parent=cls.blog_key())

    @classmethod
    def get_all(cls, order="-created"):
        return cls.all().order("-created")

    @classmethod
    def blog_key(cls, name="default"):
        return db.Key.from_path("blogs", name)

    def like_by(self, set, user):
        """ Sets whether a user likes a post or not.

        Args:
            set: A boolean value representing whether to set or unset
            user: The user who will like or not the post.

        Returns:
            Return the Like entity if it is properly set
            Return None on delete.

        """
        if user.username == self.author.username:
            return None
        like = Like.all().ancestor(self).filter('user = ', user).get()
        if not set:
            return like.delete()
        else:
            return like or Like.like(user, self)

    def is_liked_by(self, user):
        like = Like.all().ancestor(self).filter('user = ', user).get()
        return like

    def post_comment(self, user, comment):
        return Comment.post_comment(user, self, comment)

    def get_comments(self, order="-created"):
        return Comment.all().ancestor(self).order(order)


class Like(db.Model):
    """ Google AppEngine Datastore Entity representing a user 'liking' a post.

    All Likes are created as a child of a parent Post entity.

    Properties:
        user: A reference to the user that likes the post.
    """

    user = db.ReferenceProperty(User, collection_name="likes_collection", 
                                required=True)

    @classmethod
    def like(cls,user, post):
        return Like(user=user, parent=post).put()


class Comment(db.Model):
    """ Google AppEngine Datastore Entity representing a comment of a post.

    Comments are created as a child of a parent Post entity.

    Properties:
        author: A reference to the user that wrote the comment.
        comment: The textual content of the comment
        created: DateTime representing the creation of the comment.
        last_modified: DateTime representing the last modified time.        
    """ 

    author = db.ReferenceProperty(User, collection_name="comments_collection", 
                                  required=True)
    comment = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    last_modified = db.DateTimeProperty(auto_now=True)

    @classmethod
    def post_comment(cls, user, post, comment):
        return Comment(author=user, comment=comment, parent=post).put()

    @classmethod
    def by_id(cls, comment_id, post):
        return cls.get_by_id(int(comment_id),parent=post)

    