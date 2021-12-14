from django.contrib import admin
from django.urls import path

from blogs.views import PostsListView, LikePostView, PostTagsView, CreatePostView, CreateBlogView

urlpatterns = [
    path('posts/', PostsListView.as_view()),
    path('like-posts/<int:pk>/', LikePostView.as_view()),
    path('tags/', PostTagsView.as_view()),
    path('create-post/', CreatePostView.as_view()),
    path('create-blog/', CreateBlogView.as_view())
]
