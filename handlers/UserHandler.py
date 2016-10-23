from BlogHandler import BlogHandler

class LoginPage(BlogHandler):
    def get(self):
        self.render("login.html")

class SignupPage(BlogHandler):
    def get(self):
        self.render("signup.html")
