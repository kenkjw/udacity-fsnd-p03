from google.appengine.ext import db
from lib.py_bcrypt import bcrypt

def hash_password(username, password):
    return bcrypt.hashpw(username + password, bcrypt.gensalt())

def check_password(username, password, hashed):
    return bcrypt.hashpw(username + password, hashed) == hashed

class User(db.Model):
    username = db.StringProperty(required = True)
    password = db.TextProperty(required = True)
    email = db.StringProperty()

    @classmethod
    def by_id(cls, uid):
        return cls.get_by_id(uid, parent = cls.users_key())

    @classmethod
    def by_name(cls, name):
        u = cls.all().filter('username =', name).get()
        return u

    @classmethod
    def register(cls, name, pw, email = None):
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
    def users_key(cls, group = 'default'):
        return db.Key.from_path('users', group)