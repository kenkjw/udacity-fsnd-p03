from BlogHandler import BlogHandler
from models.post import Post, blog_key
from models.user import User

class AllPostsPage(BlogHandler):
    def get(self):
        posts = Post.all().order('-created')
        self.render("allposts.html",posts = posts)

class SinglePostPage(BlogHandler):
    def get(self,post_id):
        post = Post.by_id(post_id)
        self.render("singlepost.html",post = post)

class NewPostPage(BlogHandler):
    def get(self):
        self.render("newpost.html")

    def post(self):
        subject = self.request.get('subject')
        content = self.request.get('content')

        if subject and content:
            p = Post(parent = blog_key(), subject = subject, content = content, author = self.user)
            p.put()
            self.redirect('/blog/%s' % str(p.key().id()))
        else:
            error = "You must fill out the form"
            self.render("newpost.html", subject = subject, content = content, error = error)

    def initialize(self, *a, **kw):
        super(NewPostPage, self).initialize(*a, **kw)
        if not self.user:
            self.redirect("/login",abort="True")

class OwnerPostsPage(BlogHandler):
    def get(self, name = None):
        u = name and User.by_name(name) or self.user
        if not u:
            self.params["error"] = "User not found"
            self.render("ownerpost.html")
        else:
            self.render("ownerpost.html",posts=u.posts_collection, owner=u)

    def post(self):
        subject = self.request.get('subject')
        content = self.request.get('content')

        if subject and content:
            p = Post(parent = blog_key(), subject = subject, content = content)
            p.put()
            self.redirect('/blog/%s' % str(p.key().id()))
        else:
            error = "You must fill out the form"
            self.render("newpost.html", subject = subject, content = content, error = error)


class EditPostPage(BlogHandler):
    def get(self):
        if self.user:
            self.render("newpost.html")

    def post(self):
        subject = self.request.get('subject')
        content = self.request.get('content')

        if subject and content:
            p = Post(parent = blog_key(), subject = subject, content = content)
            p.put()
            self.redirect('/blog/%s' % str(p.key().id()))
        else:
            error = "You must fill out the form"
            self.render("newpost.html", subject = subject, content = content, error = error)

    def initialize(self, *a, **kw):
        super(EditPostPage, self).initialize(*a, **kw)
        if not self.user:
            self.redirect("/login",abort="True")

class DeletePostPage(BlogHandler):
    def post(self):
        subject = self.request.get('subject')
        content = self.request.get('content')

        if subject and content:
            p = Post(parent = blog_key(), subject = subject, content = content)
            p.put()
            self.redirect('/blog/%s' % str(p.key().id()))
        else:
            error = "You must fill out the form"
            self.render("newpost.html", subject = subject, content = content, error = error)

    def initialize(self, *a, **kw):
        super(DeletePostPage, self).initialize(*a, **kw)
        if not self.user:
            self.redirect("/login",abort="True")

