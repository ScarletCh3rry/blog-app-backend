from django.contrib import admin
from django.urls import path

from blogs.views import PostsListView

urlpatterns = [
    path('posts/', PostsListView.as_view())
]
