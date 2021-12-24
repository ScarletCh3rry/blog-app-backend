from django.db.models import Count
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from users.get_domain import get_web_url
from users.models import CustomUser


class TokenWithUsernameSerializer(TokenObtainPairSerializer):
    def get_token(self, user: CustomUser):
        token = super().get_token(user)
        token['name'] = user.login
        token['avatar'] = get_web_url(self.context['request']) + user.avatar.url
        return token


class UserSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'login',
            'email',
            'last_login',
            'date_joined',
            'avatar',
            'posts_count',
            'id'
        ]

    posts_count = SerializerMethodField()

    def get_posts_count(self, instance: CustomUser):
        return instance.blogs.aggregate(Count('posts'))['posts__count']


class RegisterSerializer(ModelSerializer):
    password = serializers.CharField(min_length=4, max_length=25, write_only=True)

    class Meta:
        model = CustomUser
        fields = [
            'login',
            'email',
            'avatar',
            'password'
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }

        def create(self, validated_data):
            return CustomUser.objects.create_user(login=validated_data['login'], password=validated_data['password'], avatar=validated_data['avatar'])

