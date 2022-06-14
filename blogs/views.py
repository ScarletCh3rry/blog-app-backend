from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters
from rest_framework.exceptions import PermissionDenied
from rest_framework.filters import SearchFilter
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from blogs.filters import PostFilterSet
from blogs.models import PostItem, UserPostRelation, Tag, Blog, Subscription, Comment, PassedQuestion, Quiz, Answer
from blogs.permissions import OnlyOwnPost
from blogs.serializers import PostSerializer, PostLikeSerializer, TagSerializer, CreatePostSerializer, \
    CreateBlogSerializer, BlogSerializer, FullBlogSerializer, SubscriptionSerializer, SubscriptionStatusSerializer, \
    PostCommentSerializer, QuizSerializer, QuestionSerializer, AnswerSerializer, PassedQuestionSerializer, \
    CreateQuestionSerializer, EditPostSerializer
from users.models import CustomUser


class PostsListView(generics.ListAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = PostItem.objects.all().order_by('-creation_date', 'views_count')
    serializer_class = PostSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['title', 'description']
    filterset_class = PostFilterSet

    def get_serializer(self, posts, *args, **kwargs):
        serializer = super().get_serializer(posts, *args, **kwargs)
        if self.request.user.is_authenticated:
            for post in posts:
                relation, _ = UserPostRelation.objects.get_or_create(user=self.request.user, post=post)
                relation.watched = True
                relation.save()
        return serializer


class LikePostView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = UserPostRelation.objects.all()
    serializer_class = PostLikeSerializer

    def get_object(self):
        obj, _ = UserPostRelation.objects.get_or_create(user=self.request.user, post_id=self.kwargs['pk'])
        return obj


class PostTagsView(generics.ListAPIView):
    queryset = Tag.objects.all().order_by('name')
    serializer_class = TagSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'slug']


class CreatePostView(generics.CreateAPIView):
    serializer_class = CreatePostSerializer
    permission_classes = [IsAuthenticated]




class CreateBlogView(generics.CreateAPIView):
    serializer_class = CreateBlogSerializer
    permission_classes = [IsAuthenticated]


class UserBlogsView(generics.ListAPIView):
    serializer_class = FullBlogSerializer

    def get_queryset(self):
        return Blog.objects.filter(owner__login=self.kwargs['login'])


class BlogView(generics.RetrieveAPIView):
    serializer_class = FullBlogSerializer
    queryset = Blog.objects.all()

    def get_object(self):
        obj = get_object_or_404(self.queryset, owner__login=self.kwargs['login'], slug=self.kwargs['slug'])
        return obj


class DeleteBlogView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.login != self.kwargs['login']:
            raise PermissionDenied('Вы не можете удалить чужой блог')
        return Blog.objects.all()

    def get_object(self):
        return Blog.objects.get(owner__login=self.kwargs['login'],
                                slug=self.kwargs['slug'])


class PostView(generics.RetrieveAPIView):
    serializer_class = PostSerializer
    queryset = PostItem.objects.all()

    def get_object(self):
        obj = get_object_or_404(self.queryset, blog__owner__login=self.kwargs['login'],
                                blog__slug=self.kwargs['blog_slug'],
                                slug=self.kwargs['post_slug'])
        return obj


class SubscriptionView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['title', 'description']
    filterset_class = PostFilterSet

    def get_queryset(self):
        user = CustomUser.objects.get(login=self.kwargs['login'])
        return PostItem.objects.filter(
            blog__owner__in=user.subscriptions.filter(subscription_status=True).values_list('user_you_subscribed_to',
                                                                                            flat=True))


class SubscriptionUpdateView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionStatusSerializer

    def get_object(self):
        if self.request.user.login == self.kwargs['login']:
            raise PermissionDenied('Вы не можете подписаться на себя')
        obj, _ = Subscription.objects.get_or_create(user_who_subscribed=self.request.user,
                                                    user_you_subscribed_to=CustomUser.objects.get(
                                                        login=self.kwargs['login']))
        return obj


class DeletePostView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.login != self.kwargs['login']:
            raise PermissionDenied('Вы не можете удалить чужой пост')
        return PostItem.objects.all()

    def get_object(self):
        return PostItem.objects.get(blog__owner__login=self.kwargs['login'],
                                    blog__slug=self.kwargs['blog_slug'],
                                    slug=self.kwargs['post_slug'])


class EditPostView(generics.UpdateAPIView):
    serializer_class = EditPostSerializer
    lookup_field = 'slug'
    lookup_url_kwarg = 'post_slug'
    queryset = PostItem.objects.all()

    def get_object(self):
        if self.request.user.login != self.kwargs["login"]:
            raise PermissionDenied(detail="You can't change posts of other persons", code=None)
        return get_object_or_404(self.queryset, blog__owner__login=self.kwargs["login"],
                                 blog__slug=self.kwargs['blog_slug'],
                                 slug=self.kwargs['post_slug'])

    # def patch(self, request, *args, **kwargs):
    #     image = self.request.data.get('image')
    #     post = PostItem.objects.filter(blog__owner__login=self.kwargs['login'],
    #                                    blog__slug=self.kwargs['blog_slug'],
    #                                    slug=self.kwargs['post_slug']).first()
    #     post.image = image
    #     post.save()
    #     return Response(post.image)


    # def get_queryset(self):
    #     return PostItem.objects.get(blog__owner__login=self.kwargs['login'],
    #                                 blog__slug=self.kwargs['blog_slug'],
    #                                 slug=self.kwargs['post_slug'])


class CommentsView(generics.ListAPIView):
    serializer_class = PostCommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(post__slug=self.kwargs['post_slug'])


class CreateCommentView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostCommentSerializer


class CreateQuizView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, OnlyOwnPost]
    serializer_class = QuizSerializer


class QuizListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = QuizSerializer

    # queryset = Quiz.objects.all()

    def get_queryset(self):
        return Quiz.objects.filter(post__slug=self.kwargs['post_slug'])


class QuizItemView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = QuizSerializer
    lookup_field = 'slug'
    lookup_url_kwarg = 'quiz_slug'

    def get_queryset(self):
        return Quiz.objects.filter(slug=self.kwargs['quiz_slug'])


class CreateQuestionView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, OnlyOwnPost]
    serializer_class = CreateQuestionSerializer


# class QuestionsView(generics.ListAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = QuestionSerializer


# class AnswersView(generics.ListAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = AnswerSerializer


class PassedQuestionView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        answer = Answer.objects.get(id=self.request.data['answer'])
        user = CustomUser.objects.get(login=self.kwargs['login'])
        passed_question = PassedQuestion.objects.filter(user=user, answer__question=answer.question).first()
        if passed_question is None:
            passed_question = PassedQuestion.objects.create(user=user, answer=answer)
        passed_question.answer = answer
        passed_question.save()
        return Response(answer.answer)


class DeleteQuizView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.login != self.kwargs['login']:
            raise PermissionDenied('Вы не можете удалить чужой квиз')
        return Quiz.objects.all()

    def get_object(self):
        return Quiz.objects.get(post__blog__owner__login=self.kwargs['login'],
                                post__blog__slug=self.kwargs['blog_slug'],
                                post__slug=self.kwargs['post_slug'],
                                slug=self.kwargs['quiz_slug'])
