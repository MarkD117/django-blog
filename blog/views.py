from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic, View
from django.http import HttpResponseRedirect
from .models import Post
from .forms import CommentForm
from django.contrib import messages


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
                'commented': False,
                'liked': liked,
                'comment_form': CommentForm()
            },
        )

    def post(self, request, slug, *args, **kwargs):
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.filter(approved=True).order_by('created_on')
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        # Gets all of the data from the comment form
        comment_form = CommentForm(data=request.POST)

        # is.valid() checks if information has
        # been submitted to the form.
        if comment_form.is_valid():
            # sets email and username automatically
            comment_form.instance.email = request.user.email
            comment_form.instance.name = request.user.username
            # saves comment but does not commit yet until
            # a post is assigned to it.
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
            messages.success(request, 'Your comment was added successfully!')
        else:
            # if the comment form is not valid, an
            # empty comment form instance is returned.
            comment_form = CommentForm()

        return render(
            request,
            'post_detail.html',
            {
                'post': post,
                'comments': comments,
                'commented': True,
                'liked': liked,
                'comment_form': CommentForm()
            },
        )

class PostLike(View):
    
    def post(self, request, slug):
        post = get_object_or_404(Post, slug=slug)

        # checking to see if the post has already been liked
        if post.likes.filter(id=request.user.id).exists():
            # Removes like
            post.likes.remove(request.user)
        else:
            # add like if it does not exists
            post.likes.add(request.user)

        # liking or unliking a post will reload the post_detail page and update the like
        return HttpResponseRedirect(reverse('post_detail', args=[slug]))
