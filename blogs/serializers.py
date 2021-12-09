from rest_framework.serializers import ModelSerializer

from blogs.models import PostItem, Tag, Blog
from users.models import CustomUser


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = [
            'name',
            'slug',
        ]


class CustomUserSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'login',
            'avatar',
        ]


class BlogSerializer(ModelSerializer):
    class Meta:
        model = Blog
        fields = [
            'title',
            'owner',
        ]

    owner = CustomUserSerializer(read_only=True)


class PostSerializer(ModelSerializer):
    class Meta:
        model = PostItem
        fields = [
            'title',
            'description',
            'tags',
            'creation_date',
            'likes_count',
            'comments_count',
            'quizzes_count',
            'views_count',
            'blog',
        ]
        read_only_fields = ['likes_count', 'comments_count', 'quizzes_count', 'views_count']

    blog = BlogSerializer(read_only=True)
    tags = TagSerializer(read_only=True, many=True)
