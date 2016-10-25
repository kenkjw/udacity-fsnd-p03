from BlogHandler import BlogHandler, AuthBlogHandler
from models.post import Post, Comment
from models.user import User
from utils import errors

class AllPostsPage(BlogHandler):
    def get(self):
        posts = Post.all().order('-created')
        self.render("allposts.html",posts = posts)

class SinglePostPage(BlogHandler):
    def get(self,post_id):
        post = Post.by_id(post_id)
        self.render("singlepost.html",post = post)

class OwnerPostsPage(BlogHandler):
    def get(self, name = None):
        u = name and User.by_name(name)
        if not u:
            if self.user:
                if name:
                    self.redirect_error("/blog","USER_NOT_FOUND")
                else:
                    self.render("ownerpost.html",posts=self.user.posts_collection, owner=self.user)
            else:
                self.redirect_error("/","USER_NOT_FOUND")
        else:
            self.render("ownerpost.html",posts=u.posts_collection, owner=u)

class NewPostPage(AuthBlogHandler):
    def get(self):
        self.render("newpost.html")

    def post(self):
        subject = self.request.get('subject')
        content = self.request.get('content')

        if subject and content:
            p = Post(parent = Post.blog_key(), subject = subject, content = content, author = self.user)
            p.put()
            self.redirect('/blog/%s' % str(p.key().id()))
        else:
            error = errors.get_str("POST_INCOMPLETE_FORM")
            self.render("newpost.html", subject = subject, content = content, error = error)

class EditPostPage(AuthBlogHandler):
    def get(self,post_id):
        post = Post.by_id(post_id)
        if post: 
            self.render("editpost.html", post=post)
        else:
            self.redirect_error("/blog","POST_NOT_FOUND")

    def post(self,post_id):
        subject = self.request.get('subject')
        content = self.request.get('content')

        post = Post.by_id(post_id)
        if not post:
            self.redirect_error("/blog","POST_NOT_FOUND")
        elif post.author.username != self.user.username:
            self.redirect_error("/blog/%s" % str(post.key().id()),
                                "POST_NO_PERMISSION_EDIT")
        elif subject and content:
            post.subject = subject
            post.content = content
            post.put()
            self.redirect('/blog/%s' % str(post.key().id()))
        else:
            error = errors.get_str("POST_INCOMPLETE_FORM")
            self.render("editpost.html", post=post, subject=subject, content=content, error=error)


class DeletePostPage(AuthBlogHandler):
    def post(self, post_id):
        post = Post.by_id(post_id)
        if not post:
            self.redirect_error("/blog","POST_NOT_FOUND")
        elif post.author.username != self.user.username:
            self.redirect_error("/blog/"+post_id,
                                "POST_NO_PERMISSION_DELETE")
        else:
            post.delete()
            self.redirect("/blog")

class LikePostPage(AuthBlogHandler):
    def get(self, post_id, like = True):
        post = Post.by_id(post_id)
        if not post:
            self.redirect_error("/blog","POST_NOT_FOUND")
        elif post.author.username == self.user.username:
            self.redirect_error("/blog/"+post_id,POST_LIKE_OWN)
        else:
            post.like_by(like, self.user)
            self.redirect("/blog/"+post_id)

class UnlikePostPage(LikePostPage):
    def get(self, post_id):
        super(UnlikePostPage, self).get(post_id, False)

class CommentPostPage(AuthBlogHandler):
    def post(self, post_id):
        post = Post.by_id(post_id)

        content = self.request.get('content')
        
        if not post:
            self.redirect_error("/blog","POST_NOT_FOUND")
        elif content:
            post.post_comment(self.user, content)
            self.redirect("/blog/"+post_id)
        else:
            self.redirect_error("/blog/"+post_id,"POST_INCOMPLETE_FORM")

class CommentEditPostPage(AuthBlogHandler):
    def post(self, post_id):
        post = Post.by_id(post_id)
        content = self.request.get('content')
        
        if not post:
            self.redirect_error("/blog","POST_NOT_FOUND")

class CommentDeletePostPage(AuthBlogHandler):
    def post(self, post_id,comment_id):
        post = Post.by_id(post_id)
        comment = Comment.by_id(comment_id,post)

        if not post:
            self.redirect_error("/blog","POST_NOT_FOUND")
        elif not comment:
            self.redirect_error("/blog/"+post_id,"COMMENT_NOT_FOUND")
        elif comment.author.username != self.user.username:
            self.redirect_error("/blog/"+post_id,"COMMENT_NO_PERMISSION_DELETE")
        else:
            comment.delete()
            self.redirect("/blog/"+post_id)
