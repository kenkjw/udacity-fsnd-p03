import webapp2

import handlers.PostHandler as PostHandler
import handlers.UserHandler as UserHandler



app = webapp2.WSGIApplication([
    ('/', PostHandler.AllPostsPage),
    ('/blog', PostHandler.AllPostsPage),
    ('/blog/(\d+)', PostHandler.SinglePostPage),
    ('/blog/new', PostHandler.NewPostPage),
    ('/login', UserHandler.LoginPage),
    ('/signup', UserHandler.SignupPage),
    ('/logout', UserHandler.LogoutPage),
    ('/welcome', UserHandler.WelcomePage)
], debug=True)
