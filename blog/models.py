from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

STATUS = ((0, "Draft"), (1, "Published"))


class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    # on_delete... means if the author of the post is deleted,
    # all related posts will also be deleted
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="blog_posts"
    )
    featured_image = CloudinaryField('image', default='placeholder')
    excerpt = models.TextField(blank=True)
    updated_on = models.DateTimeField(auto_now=True)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    likes = models.ManyToManyField(
        User, related_name='blogpost_like', blank=True)

    class Meta:
        # order  our posts on the created_on field,
        # minus sign means to use descending order,
        # meaning newest posts will be listed 1st
        ordering = ["-created_on"]

    # returns string representation of an object
    def __str__(self):
        return self.title

    # returns the total number of likes on a post
    def number_of_likes(self):
        return self.likes.count()


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name="comments")
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    class Meta:
        # order  our posts on the created_on field,
        # ordered in ascending order, meaning newest
        # comments will be listed 1st
        ordering = ["created_on"]

    def __str__(self):
        return f"Comment {self.body} by {self.name}"
