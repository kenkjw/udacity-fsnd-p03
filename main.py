import webapp2

import handlers.PostHandler as PostHandler
import handlers.UserHandler as UserHandler



app = webapp2.WSGIApplication([
    ('/', PostHandler.AllPostsPage),
    ('/user/([a-zA-Z0-9_-]+)', PostHandler.OwnerPostsPage),
    ('/blog', PostHandler.OwnerPostsPage),
    ('/blog/(\d+)', PostHandler.SinglePostPage),
    ('/blog/(\d+)/like', PostHandler.LikePostPage),
    ('/blog/(\d+)/unlike', PostHandler.UnlikePostPage),
    ('/blog/new', PostHandler.NewPostPage),
    ('/blog/(\d+)/edit', PostHandler.EditPostPage),
    ('/blog/(\d+)/delete', PostHandler.DeletePostPage),
    ('/login', UserHandler.LoginPage),
    ('/signup', UserHandler.SignupPage),
    ('/logout', UserHandler.LogoutPage),
    ('/welcome', UserHandler.WelcomePage)
], debug=True)
