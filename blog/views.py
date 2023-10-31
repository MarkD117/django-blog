from django.shortcuts import render, get_object_or_404
from django.views import generic, View
from .models import Post


class PostList(generic.ListView):
    model = Post
    # queryset value set to the content of our post model
    # filtered with a status of 1 meaning it is published
    # and ordered by created on in descending order
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'index.html'
    # limits the number of pages that can appear on one page to 6
    paginate_by = 6


class PostDetail(View):

    def get(self, request, slug, *args, **kwargs):
        queryset = Post.objects.filter(status=1)
        # gets published post with the correct slug
        post = get_object_or_404(queryset, slug=slug)
        # gets comments of post ordered by oldest 1st
        comments = post.comments.filter(approved=True).order_by('created_on')
        liked = False
        # if the user id exists to say a user has liked
        # the post the liked value will be set to True
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        # sending all information to render method
        return render(
            # sending request
            request,
            # specifying template required
            'post_detail.html',
            # using a dictionary to supply our context
            {
                'post': post,
                'comments': comments,
                'liked': liked
            },
        )
