import re
from string import letters
from google.appengine.ext import db
from lib.py_bcrypt import bcrypt


class User(db.Model):
    """ Google AppEngine Datastore Entity representing a User of the blog.

    This class also provides methods dealing with registering and logging in,
    along with methods for validating its properties.

    Properties:
        username: A string representing the username of the User. Must
                  be 3-20 letters long and only letters, numbers, and -_
        password: A string representing the user's password.
        email: An optional property representing the user's email.
    """
    
    username = db.StringProperty(required=True)
    password = db.TextProperty(required=True)
    email = db.StringProperty()

    _USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
    _PASS_RE = re.compile(r"^.{3,20}$")
    _EMAIL_RE  = re.compile(r"^[\S]+@[\S]+\.[\S]+$")

    @classmethod
    def by_id(cls, uid):
        return cls.get_by_id(uid, parent=cls.users_key())

    @classmethod
    def by_name(cls, name):
        u = cls.all().filter("username = ", name).get()
        return u

    @classmethod
    def register(cls, name, pw, email=None):
        return User(parent = cls.users_key(),
            username = name,
            password = hash_password(name, pw),
            email = email)

    @classmethod
    def login(cls, name, pw):
        u = cls.by_name(name)
        if u and check_password(name, pw, u.password):
            return u
    
    @classmethod
    def users_key(cls, group="default"):
        return db.Key.from_path("users", group)
    
    @classmethod
    def valid_username(cls, username):
        return username and cls._USER_RE.match(username)

    @classmethod
    def valid_password(cls, password):
        return password and cls._PASS_RE.match(password)

    @classmethod
    def valid_email(cls, email):
        return not email or cls._EMAIL_RE.match(email)


# Helper functions for dealing with hashing and checking passwords

def hash_password(username, password):
    return bcrypt.hashpw(username + password, bcrypt.gensalt())


def check_password(username, password, hashed):
    return bcrypt.hashpw(username + password, hashed) == hashed



