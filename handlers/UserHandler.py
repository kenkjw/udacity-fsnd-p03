from BlogHandler import BlogHandler
from models.user import User

class LoginPage(BlogHandler):
    """ Handler for logging in
    
    Allows get/post methods.''
    If the user is already logged in, redirect to blog posts
    On successful login, redirect to welcome page.

    URI:
        /login
    """
    def get(self):
        if self.user:
            self.redirect("/")
        else:
            self.render("login.html")

    def post(self):
        username = self.request.get("username")
        password = self.request.get("password")

        u = User.login(username,password)
        if u:
            self.login(u)
            self.redirect("/welcome")
        else:
            self.params["error"] = "Invalid username/password combination"
            self.render("login.html")
            
class SignupPage(BlogHandler):
    """ Handler for registering a new user.

    Allows get/post methods.
    If the user is already logged in, redirect to blog posts
    On successful signup, login and redirect to welcome page.

    URI:
        /signup
    """
    def get(self):
        if self.user:
            self.redirect("/")
        else:
            self.render("signup.html")

    def post(self):
        have_error = False
        username = self.request.get("username")
        password = self.request.get("password")
        confirm = self.request.get("confirm")
        email = self.request.get("email")
        
        self.params["username"] = username
        self.params["email"] = email
        
        # Validate the inputs

        if not User.valid_username(username):
            self.params["error_username"] = "That's not a valid username."
            have_error = True
        if not User.valid_password(password):
            self.params["error_password"] = "That wasn't a valid password."
            have_error = True
        elif password != confirm:
            self.params["error_password"] = "Your passwords didn't match."
            have_error = True
        if not User.valid_email(email):
            self.params["error_email"] = "That's not a valid email."
            have_error = True

        if have_error:
            self.render("signup.html")
        else:
            # Form validation is okay. Check if user exists before signing up.
            u = User.by_name(username)
            if u:
                msg = "That user already exists."
                self.render("signup.html", error_username = msg)
            else:
                u = User.register(username, password, email)
                u.put()
                self.login(u)
                self.redirect("/welcome")

class LogoutPage(BlogHandler):
    """ Handler for logging out.

    Allows get method.
    Doesn't require user to be signed in.
    Logs out and redirects to the signup page

    URI:
        /logout
    """    
    def get(self):
        self.logout()
        self.redirect("/signup")

class WelcomePage(BlogHandler):
    """ Handler for the welcome page.

    Allows get method.
    If the user is not logged in, redirect to signup page

    URI:
        /welcome
    """    
    def get(self):
        if self.user:
            self.render("welcome.html")
        else:
            self.redirect("/signup")

