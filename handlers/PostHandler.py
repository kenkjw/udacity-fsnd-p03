from BlogHandler import BlogHandler, AuthBlogHandler
from models.post import Post, Comment
from models.user import User
from utils import errors

class AllPostsPage(BlogHandler):
    """ Handler for displaying all blog posts

    Allows get method.
    Doesn't require authentication.

    URI:
        /
    """

    def get(self):
        posts = Post.get_all()
        self.render("allposts.html", posts=posts)

class SinglePostPage(BlogHandler):
    """ Handler for displaying a single blog post

    Allows get method.
    Doesn't require authentication.

    URI:
        /blog/{post_id}
            post_id: numeric id of the post to be displayed.
    """

    def get(self,post_id):
        post = Post.by_id(post_id)
        self.render("singlepost.html", post=post)

class OwnerPostsPage(BlogHandler):
    """ Handler for displaying all posts from a specific user.

    Allows get method.
    Doesn't require authentication.

    URI:
        /user/{username}
            username: username string of the user whose posts 
                      should be displayed
        /blog
            Displays the posts of the authenticated user.
    """

    def get(self, name = None):
        u = name and User.by_name(name)
        if not u:           # Either user not found or defaulting to self
            if self.user:   # User is authenticated
                if name:    # User was searching for other page. Display error.
                    self.redirect_error("/blog", "USER_NOT_FOUND")
                else:       # User was searching for own page. No error.
                    self.render("ownerpost.html",
                                posts=self.user.posts_collection, 
                                owner=self.user)
            else:       # Not authenticated and no user. Redirect to all posts
                self.redirect_error("/", "USER_NOT_FOUND")
        else:               # User was found
            self.render("ownerpost.html", posts=u.posts_collection, owner=u)

class NewPostPage(AuthBlogHandler):
    """ Handler for creating a new blog post.

    Allows get/post methods.
    Requires authentication.

    URI:
        /blog/new
    """    
    def get(self):
        self.render("newpost.html")

    def post(self):
        subject = self.request.get("subject")
        content = self.request.get("content")

        if subject and content:     # Forms not empty. Okay to create post.
            p = Post(parent=Post.blog_key(), subject=subject, 
                     content=content, author=self.user)
            p.put()
            self.redirect("/blog/"+str(p.key().id()))
        else:                       # Forms empty
            error = errors.get_str("POST_INCOMPLETE_FORM")
            self.render("newpost.html", subject=subject, 
                        content=content, error=error)

class EditPostPage(AuthBlogHandler):
    """ Handler for editing an existing blog post.

    Allows get/post methods.
    Requires authentication.

    URI:
        /blog/{post_id}/edit
            post_id: numeric id of the post to be edited
    """
    def get(self,post_id):
        post = Post.by_id(post_id)
        if post: 
            self.render("editpost.html", post=post)
        else:
            self.redirect_error("/blog", "POST_NOT_FOUND")

    def post(self,post_id):
        subject = self.request.get("subject")
        content = self.request.get("content")

        post = Post.by_id(post_id)
        if not post:
            self.redirect_error("/blog","POST_NOT_FOUND")
        elif post.author.username != self.user.username:   
            # Can't edit someone else's post
            self.redirect_error("/blog/" + post_id,
                                "POST_NO_PERMISSION_EDIT")
        elif not subject or not content:
            # Can't have empty form
            error = errors.get_str("POST_INCOMPLETE_FORM")
            self.render("editpost.html", post=post, subject=subject, 
                        content=content, error=error)
        else:
            post.subject = subject
            post.content = content
            post.put()
            self.redirect("/blog/" + post_id)

class DeletePostPage(AuthBlogHandler):
    """ Handler for deleting an existing blog post.

    Allows post method.
    Requires authentication.

    URI:
        /blog/{post_id}/delete
            post_id: numeric id of the post to be deleted
    """    
    def post(self, post_id):
        post = Post.by_id(post_id)
        if not post:
            self.redirect_error("/blog", "POST_NOT_FOUND")
        elif post.author.username != self.user.username:
            # Can't delete a post you don't own
            self.redirect_error("/blog/" + post_id,
                                "POST_NO_PERMISSION_DELETE")
        else:
            post.delete()
            self.redirect("/blog")

class LikePostPage(AuthBlogHandler):
    """ Handler for liking a blog post.

    Allows get method.
    Requires authentication.

    URI:
        /blog/{post_id}/like
            post_id: numeric id of the post to be liked
    """    
    def get(self, post_id, like=True):
        post = Post.by_id(post_id)
        if not post:
            self.redirect_error("/blog", "POST_NOT_FOUND")
        elif post.author.username == self.user.username:
            # Can't like a post you own
            self.redirect_error("/blog/" + post_id, "POST_LIKE_OWN")
        else:
            post.like_by(like, self.user)
            self.redirect("/blog/" + post_id)

class UnlikePostPage(LikePostPage):
    """ Handler for unliking a blog post.

    Extends LikePostPage and calls super method with different parameter.
    TODO: Adjust route to be handled with LikePostPage.

    URI:
        /blog/{post_id}/unlike
            post_id: numeric id of the post to be unliked
    """    
    def get(self, post_id):
        super(UnlikePostPage, self).get(post_id, False)

class CommentPostPage(AuthBlogHandler):
    """ Handler for posting a comment to a blog post.

    Allows post method.
    Requires authentication.

    URI:
        /blog/{post_id}/comment
            post_id: numeric id of the post
    """    
    def post(self, post_id):
        post = Post.by_id(post_id)
        content = self.request.get("comment")
        
        if not post:
            self.redirect_error("/blog", "POST_NOT_FOUND")
        elif not content:
            # Can't have an empty form
            self.redirect_error("/blog/" + post_id, "POST_INCOMPLETE_FORM")
        else:
            post.post_comment(self.user, content)
            self.redirect("/blog/" + post_id)

class CommentEditPostPage(AuthBlogHandler):
    """ Handler for editing an existing comment.

    Allows post method.
    Requires authentication.

    URI:
        /blog/{post_id}/comment/{comment_id}/edit
            post_id: numeric id of the post
            comment_id: numeric id of the comment to be edited
    """    
    def post(self, post_id, comment_id):
        post = Post.by_id(post_id)
        comment = Comment.by_id(comment_id, post)
        content = self.request.get("comment")

        if not post:
            self.redirect_error("/blog", "POST_NOT_FOUND")
        elif not comment:
            self.redirect_error("/blog/" + post_id, "COMMENT_NOT_FOUND")
        elif comment.author.username != self.user.username:
            # Can't edit someone else's comment
            self.redirect_error("/blog/" + post_id, "COMMENT_NO_PERMISSION_DELETE")
        elif not content:
            # Can't have an empty form
            self.redirect_error("/blog/" + post_id, "POST_INCOMPLETE_FORM")
        else:
            comment.comment = content
            comment.put()
            self.redirect("/blog/"+post_id)
            


class CommentDeletePostPage(AuthBlogHandler):
    """ Handler for deleting an existing comment

    Allows post methods.
    Requires authentication.

    URI:
        /blog/{post_id}/comment/{comment_id}/delete
            post_id: numeric id of the post
            comment_id: numeric id of the comment to be deleted
    """    
    def post(self, post_id,comment_id):
        post = Post.by_id(post_id)
        comment = Comment.by_id(comment_id,post)

        if not post:
            self.redirect_error("/blog","POST_NOT_FOUND")
        elif not comment:
            self.redirect_error("/blog/"+post_id,"COMMENT_NOT_FOUND")
        elif comment.author.username != self.user.username:
            # Can't delete a comment you don't own
            self.redirect_error("/blog/"+post_id,"COMMENT_NO_PERMISSION_DELETE")
        else:
            comment.delete()
            self.redirect("/blog/"+post_id)
