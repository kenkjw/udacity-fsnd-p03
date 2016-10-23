from BlogHandler import BlogHandler

class AllPostsPage(BlogHandler):
    def get(self):
        self.render("allposts.html")

class SinglePostPage(BlogHandler):
    def get(self):
        self.render("singlepost.html")

class NewPost(BlogHandler):
    def get(self):
        self.render("newpost.html")