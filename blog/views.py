from django.shortcuts import render
from django.views import generic
from .models import Post


class PostList(generic.ListView):
    model = Post
    # queryset value set to the content of our post model
    # filtered with a status of 1 meaning it is published
    # and ordered by created on in descending order
    queryset = Post.objects.filter(status=1).order_by("-created_on")
    template_name = "index.html"
    # limits the number of pages that can appear on one page to 6
    paginate_by = 6
