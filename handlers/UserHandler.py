import re
from string import letters
from BlogHandler import BlogHandler
from models.user import User

class LoginPage(BlogHandler):
    def get(self):
        if self.user:
            self.redirect('/')
        else:
            self.render("login.html")

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')

        u = User.login(username,password)
        if u:
            self.login(u)
            self.redirect('/welcome')
        else:
            self.params["error"] = "Invalid username/password combination"
            self.render("login.html")
            
        


class SignupPage(BlogHandler):
    def get(self):
        if self.user:
            self.redirect('/')
        else:
            self.render("signup.html")

    def post(self):
        have_error = False
        username = self.request.get('username')
        password = self.request.get('password')
        confirm = self.request.get('confirm')
        email = self.request.get('email')
        
        self.params['username'] = username
        self.params['email'] = email
        
        if not valid_username(username):
            self.params['error_username'] = "That's not a valid username."
            have_error = True

        if not valid_password(password):
            self.params['error_password'] = "That wasn't a valid password."
            have_error = True
        elif password != confirm:
            self.params['error_password'] = "Your passwords didn't match."
            have_error = True

        if not valid_email(email):
            self.params['error_email'] = "That's not a valid email."
            have_error = True

        if have_error:
            self.render('signup.html')
        else:
            u = User.by_name(username)
            if u:
                msg = 'That user already exists.'
                self.render('signup.html', error_username = msg)
            else:
                u = User.register(username, password, email)
                u.put()
                self.login(u)
                self.redirect('/welcome')

class LogoutPage(BlogHandler):
    def get(self):
        self.logout()
        self.redirect('/signup')

class WelcomePage(BlogHandler):
    def get(self):
        if self.user:
            self.render("welcome.html")
        else:
            self.redirect('/signup')

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
    return not email or EMAIL_RE.match(email)