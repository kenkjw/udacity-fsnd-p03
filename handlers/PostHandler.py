from BlogHandler import BlogHandler, AuthBlogHandler
from models.post import Post
from models.user import User

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
        u = name and User.by_name(name) or self.user
        if not u:
            self.params["error"] = "User not found"
            self.render("ownerpost.html")
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
            error = "You must fill out the form"
            self.render("newpost.html", subject = subject, content = content, error = error)

class EditPostPage(AuthBlogHandler):
    def get(self,post_id):
        post = Post.by_id(post_id)
        if post: 
            self.render("editpost.html", post=post)
        else:
            error = "Unable to find post"
            self.render("ownerpost.html", posts=u.posts_collection, owner=u, error=error)

    def post(self,post_id):
        subject = self.request.get('subject')
        content = self.request.get('content')

        post = Post.by_id(post_id)
        if not post:
            error = "Unable to find post"
            self.render("ownerpost.html", posts=u.posts_collection, owner=u, error=error)
        elif post.author.username != self.user.username:
            error = "You do not have the permission to edit this post"
            self.render("singlepost.html", post=post, error=error)
        elif subject and content:
            post.subject = subject
            post.content = content
            post.put()
            self.redirect('/blog/%s' % str(post.key().id()))
        else:
            error = "You must fill out the form"
            self.render("editpost.html", subject = subject, content = content, error = error)


class DeletePostPage(AuthBlogHandler):
    def post(self, post_id):
        post = Post.by_id(post_id)
        if not post:
            error = "Unable to find post"
            self.render("ownerpost.html", posts=u.posts_collection, owner=u, error=error)
        elif post.author.username != self.user.username:
            error = "You do not have the permission to delete this post"
            self.render("singlepost.html", post=post, error=error)
        else:
            post.delete()
            self.redirect("/blog")

class LikePostPage(AuthBlogHandler):
    def get(self, post_id, like = True):
        post = Post.by_id(post_id)
        if not post:
            error = "Unable to find post"
            self.render("ownerpost.html", posts=u.posts_collection, owner=u, error=error)
        elif post.author.username == self.user.username:
            error = "You cannot like your own post"
            self.render("singlepost.html", post=post, error=error)
        else:
            post.like_by(like, self.user)
            self.redirect("/blog/"+post_id)

class UnlikePostPage(LikePostPage):
    def get(self, post_id):
        super(UnlikePostPage, self).get(post_id, False)

class CommentPostPage(AuthBlogHandler):
    pass