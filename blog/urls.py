from . import views
from django.urls import path


urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
    # 'slug' keyword name matches 'slug' parameter in
    # get method of PostDetail class in blog/views.py
    # file. That is how they are linked together.
    path('<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
    path('like/<slug:slug>', views.PostLike.as_view(), name='post_like')
]
