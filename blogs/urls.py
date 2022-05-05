from django.contrib import admin
from django.urls import path

from blogs.views import PostsListView, LikePostView, PostTagsView, CreatePostView, CreateBlogView, BlogView, PostView, \
    UserBlogsView, SubscriptionView, SubscriptionUpdateView

urlpatterns = [
    path('posts/', PostsListView.as_view()),
    path('like-posts/<int:pk>/', LikePostView.as_view()),
    path('tags/', PostTagsView.as_view()),
    path('create-post/', CreatePostView.as_view()),
    path('create-blog/', CreateBlogView.as_view()),
    path('<str:login>/subscription-update/', SubscriptionUpdateView.as_view()),
    path('<str:login>/subscriptions/', SubscriptionView.as_view()),
    path('<str:login>/<str:slug>/', BlogView.as_view()),
    path('<str:login>/<str:blog_slug>/<str:post_slug>/', PostView.as_view()),
    path('<str:login>/', UserBlogsView.as_view()),
    path('posts/<str:post_slug>/', PostView.as_view()),
]
