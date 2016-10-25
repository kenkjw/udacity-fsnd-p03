import webapp2
import random
import hashlib
import hmac
import os
import jinja2
from lib import markdown
import config
from models.user import User
from utils import errors

#   Initialize jinja2 templating system and setup a Markdown filter.

template_dir = os.path.join(os.path.dirname(__file__), "../templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               autoescape=True)
md = lambda text: jinja2.Markup(markdown.Markdown().convert(jinja2.escape(text)))
jinja_env.filters["markdown"] = md


class BlogHandler(webapp2.RequestHandler):
    """ Extension of webapp2's RequestHandler.

    BlogHandler is used as the base class for all handlers in the application.
    It provides methods for subclasses to use the jinja2 templating system and
    methods dealing with authentication.

    Attributes:
        params: A dictionary of additional key-values that will be passed to
                jinja templating.

    """
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.params.update(kw)
        self.write(self.render_str(template, **self.params))

    def set_secure_cookie(self, name, val):
        cookie_val = _make_secure_val(val)
        self.response.headers.add_header(
            "Set-Cookie",
            "%s=%s; Path=/" % (name, cookie_val))

    def read_secure_cookie(self, name):
        cookie_val = self.request.cookies.get(name)
        return cookie_val and _check_secure_val(cookie_val)

    def login(self, user):
        self.set_secure_cookie("user_id", str(user.key().id()))

    def logout(self):
        self.response.headers.add_header("Set-Cookie", "user_id=; Path=/")

    def redirect_error(self,uri,error):
        """ Attaches a query string to the end of a redirect uri

        This method is used for preserving an error message after a redirect.
        """
        self.redirect(uri+"?error="+errors.get(error),abort=True)

    def initialize(self, *a, **kw):
        """ Initialize some state from the request.

        Check if the user is authenticated. If so, store user information.
        Also, check if the user was redirected with an error.
        """
        webapp2.RequestHandler.initialize(self, *a, **kw)
        uid = self.read_secure_cookie("user_id")
        self.user = uid and User.by_id(int(uid))
        self.params = dict()
        self.params["user"] = self.user
        if self.request.get("error"):
            self.params["error"] = errors.get(self.request.get("error"))

class AuthBlogHandler(BlogHandler):
    """ Extension of the base BlogHandler.

    AuthBlogHandler differs from BlogHandler in that it will automatically
    redirect a user to the login page if the user is not logged in.

    Handlers that require the user to be logged in should inherit this class.

    """    
    def initialize(self, *a, **kw):
        super(AuthBlogHandler, self).initialize(*a, **kw)
        if not self.user:
            self.redirect("/login",abort="True")


# Helper methods used for securing cookie data.
def _make_secure_val(val):
    return "%s|%s" % (val, hmac.new(config.SECRET, val).hexdigest())

def _check_secure_val(secure_val):
    val = secure_val.split("|")[0]
    if secure_val == _make_secure_val(val):
        return val