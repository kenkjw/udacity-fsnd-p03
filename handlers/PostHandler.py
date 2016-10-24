from BlogHandler import BlogHandler
from models.post import Post, blog_key


class AllPostsPage(BlogHandler):
    def get(self):
        posts = Post.get_all()
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
            p = Post(parent = blog_key(), subject = subject, content = content)
            p.put()
            self.redirect('/blog/%s' % str(p.key().id()))
        else:
            error = "You must fill out the form"
            self.render("newpost.html", subject = subject, content = content, error = error)
