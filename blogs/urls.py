from django.contrib import admin
from django.urls import path

from blogs.views import PostsListView, LikePostView, PostTagsView, CreatePostView, CreateBlogView, BlogView, PostView, \
    UserBlogsView, SubscriptionView, SubscriptionUpdateView, DeletePostView, CommentsView, CreateCommentView, \
    CreateQuizView, QuizListView, CreateQuestionView, QuizItemView, PassedQuestionView, DeleteQuizView, DeleteBlogView

urlpatterns = [
    path('posts/', PostsListView.as_view()),
    path('like-posts/<int:pk>/', LikePostView.as_view()),
    path('tags/', PostTagsView.as_view()),
    path('create-post/', CreatePostView.as_view()),
    path('create-blog/', CreateBlogView.as_view()),
    path('<str:login>/subscription-update/', SubscriptionUpdateView.as_view()),
    path('<str:login>/subscriptions/', SubscriptionView.as_view()),
    path('<str:login>/<str:slug>/', BlogView.as_view()),
    path('<str:login>/<str:slug>/delete-blog/', DeleteBlogView.as_view()),
    path('<str:login>/<str:blog_slug>/<str:post_slug>/', PostView.as_view()),
    path('<str:login>/<str:blog_slug>/<str:post_slug>/comments/', CommentsView.as_view()),
    path('<str:login>/<str:blog_slug>/<str:post_slug>/create-comment/', CreateCommentView.as_view()),
    path('<str:login>/', UserBlogsView.as_view()),
    path('<str:login>/<str:blog_slug>/<str:post_slug>/delete-post/', DeletePostView.as_view()),
    path('<str:login>/<str:blog_slug>/<str:post_slug>/create-quiz/', CreateQuizView.as_view()),
    path('<str:login>/<str:blog_slug>/<str:post_slug>/quizes/', QuizListView.as_view()),
    path('<str:login>/<str:blog_slug>/<str:post_slug>/<str:quiz_slug>/', QuizItemView.as_view()),
    path('<str:login>/<str:blog_slug>/<str:post_slug>/<str:quiz_slug>/delete-quiz/', DeleteQuizView.as_view()),
    path('<str:login>/<str:blog_slug>/<str:post_slug>/create-quiz/create-question/', CreateQuestionView.as_view()),
    path('<str:login>/<str:blog_slug>/<str:post_slug>/<str:quiz_slug>/passed-question/', PassedQuestionView.as_view()),
    # path('<str:login>/<str:blog_slug>/<str:post_slug>/quizes/questions/', QuestionsView.as_view()),
    # path('<str:login>/<str:blog_slug>/<str:post_slug>/quizes/questions/answers/', AnswersView.as_view()),
    # path('<str:login>/<str:blog_slug>/<str:post_slug>/quizes/questions/answers/passed-question/', PassedQuestionView.as_view()),
]
