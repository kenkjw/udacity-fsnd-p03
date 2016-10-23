from BlogHandler import BlogHandler
import models.post as Post

class AllPostsPage(BlogHandler):
    def get(self):
        self.render("allposts.html")

class SinglePostPage(BlogHandler):
    def get(self,post_id):
        self.render("singlepost.html")

class NewPostPage(BlogHandler):
    def get(self):
        self.render("newpost.html")

    def post(self):
        subject = self.request.get('subject')
        content = self.request.get('content')

        if subject and content:
            p = Post.Post(parent = Post.blog_key(), subject = subject, content = content)
            p.put()
            self.redirect('/blog/%s' % str(p.key().id()))
        else:
            error = "You must fill out the form"
            self.render("newpost.html", subject = subject, content = content, error = error)
