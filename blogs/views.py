from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from blogs.filters import PostFilterSet
from blogs.models import PostItem, UserPostRelation, Tag, Blog
from blogs.serializers import PostSerializer, PostLikeSerializer, TagSerializer, CreatePostSerializer, \
    CreateBlogSerializer, BlogSerializer, FullBlogSerializer
from users.models import CustomUser


class PostsListView(generics.ListAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = PostItem.objects.all().order_by('views_count')
    serializer_class = PostSerializer
    filter_backends = [DjangoFilterBackend]
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
