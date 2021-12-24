from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from blogs.models import PostItem, Tag, Blog, UserPostRelation, Comment
from users.models import CustomUser


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = [
            'name',
            'slug',
            'id',
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
        read_only_fields = ('slug',)
        fields = [
            'title',
            'owner',
            'description',
            'slug',
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
            'id',
            'is_liked'
        ]
        read_only_fields = ['likes_count', 'comments_count', 'quizzes_count', 'views_count']

    likes_count = SerializerMethodField()
    views_count = SerializerMethodField()
    comments_count = SerializerMethodField()
    is_liked = SerializerMethodField()

    def get_likes_count(self, instance: PostItem):
        return UserPostRelation.objects.filter(post=instance, like=True).count()

    def get_views_count(self, instance: PostItem):
        return UserPostRelation.objects.filter(post=instance, watched=True).count()

    def get_comments_count(self, instance: PostItem):
        return Comment.objects.filter(post=instance).count()

    def get_is_liked(self, instance: PostItem):
        if not self.context['request'].user.is_authenticated:
            return False
        return UserPostRelation.objects.filter(post=instance, like=True, user=self.context['request'].user).exists()

    blog = BlogSerializer(read_only=True)
    tags = TagSerializer(read_only=True, many=True)


class FullBlogSerializer(ModelSerializer):
    class Meta:
        model = Blog
        fields = [
            'posts',
            'title',
            'owner',
            'description',
            'slug',
        ]

    posts = PostSerializer(read_only=True, many=True)
    owner = CustomUserSerializer(read_only=True)


class PostLikeSerializer(ModelSerializer):
    class Meta:
        model = UserPostRelation
        fields = [
            'like',
            'watched'
        ]


class PostCommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            'text',
            'owner',
            'post'
        ]

    owner = CustomUserSerializer(read_only=True)


class CreatePostSerializer(ModelSerializer):
    class Meta:
        model = PostItem
        fields = [
            'title',
            'description',
            'tags',
            'blog',
            'slug',
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['tags'] = TagSerializer(Tag.objects.filter(id__in=representation['tags']), many=True).data
        representation['blog'] = BlogSerializer(Blog.objects.get(id=representation['blog'])).data
        return representation

    def validate(self, attrs):
        if not self.context['request'].user.blogs.filter(id=attrs['blog'].id).exists():
            raise serializers.ValidationError({'blog': 'Низя саздавать пасты для блогафф'})
        return super().validate(attrs)


class CreateBlogSerializer(ModelSerializer):
    class Meta:
        model = Blog
        fields = [
            'title',
            'owner',
            'description',
            'slug',
        ]
        read_only_fields = ['owner', 'slug']

    owner = CustomUserSerializer(read_only=True)

    def save(self, **kwargs):
        return super().save(**kwargs, owner=self.context['request'].user)
