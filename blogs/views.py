from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters
from rest_framework.exceptions import PermissionDenied
from rest_framework.filters import SearchFilter
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from blogs.filters import PostFilterSet
from blogs.models import PostItem, UserPostRelation, Tag, Blog, Subscription
from blogs.serializers import PostSerializer, PostLikeSerializer, TagSerializer, CreatePostSerializer, \
    CreateBlogSerializer, BlogSerializer, FullBlogSerializer, SubscriptionSerializer, SubscriptionStatusSerializer
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
