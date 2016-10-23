import webapp2

import handlers.PostHandler as PostHandler
import handlers.UserHandler as UserHandler



app = webapp2.WSGIApplication([
    ('/', PostHandler.AllPostsPage),
    ('/login', UserHandler.LoginPage),
    ('/signup', UserHandler.SignupPage)
], debug=True)
