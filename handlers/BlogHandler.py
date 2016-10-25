import webapp2
import random
import hashlib
import hmac
import os
import jinja2
from lib import markdown
import config
from models.user import User

template_dir = os.path.join(os.path.dirname(__file__), '../templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)
md = markdown.Markdown()
jinja_env.filters['markdown'] = lambda text: jinja2.Markup(md.convert(text))


class BlogHandler(webapp2.RequestHandler):
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
            'Set-Cookie',
            '%s=%s; Path=/' % (name, cookie_val))

    def read_secure_cookie(self, name):
        cookie_val = self.request.cookies.get(name)
        return cookie_val and _check_secure_val(cookie_val)

    def login(self, user):
        self.set_secure_cookie('user_id', str(user.key().id()))

    def logout(self):
        self.response.headers.add_header('Set-Cookie', 'user_id=; Path=/')

    def initialize(self, *a, **kw):
        webapp2.RequestHandler.initialize(self, *a, **kw)
        uid = self.read_secure_cookie('user_id')
        self.user = uid and User.by_id(int(uid))
        self.params = dict()
        self.params['user'] = self.user

class AuthBlogHandler(BlogHandler):
    def initialize(self, *a, **kw):
        super(AuthBlogHandler, self).initialize(*a, **kw)
        if not self.user:
            self.redirect("/login",abort="True")

def _make_secure_val(val):
    return '%s|%s' % (val, hmac.new(config.secret, val).hexdigest())

def _check_secure_val(secure_val):
    val = secure_val.split('|')[0]
    if secure_val == _make_secure_val(val):
        return val