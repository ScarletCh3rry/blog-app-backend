from django.db.models import Count
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken

from users.get_domain import get_web_url
from users.models import CustomUser


class TokenWithUsernameSerializer(TokenObtainPairSerializer):
    def get_token(self, user: CustomUser):
        token = super().get_token(user)
        token['name'] = user.login
        token['avatar'] = get_web_url(self.context['request']) + user.avatar.url
        return token


class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        request = self.context['request']
        web_url = get_web_url(request)
        refresh = RefreshToken(attrs['refresh'])
        access_token = refresh.access_token
        user = CustomUser.objects.get(id=access_token['user_id'])
        access_token['name'] = user.login
        access_token['avatar'] = web_url + user.avatar.url
        data = {'access': str(access_token)}
        if api_settings.ROTATE_REFRESH_TOKENS:
            if api_settings.BLACKLIST_AFTER_ROTATION:
                try:
                    # Attempt to blacklist the given refresh token
                    refresh.blacklist()
                except AttributeError:
                    # If blacklist app not installed, `blacklist` method will
                    # not be present
                    pass

            refresh.set_jti()
            refresh.set_exp()

            data['refresh'] = str(refresh)
        return data


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


class UserEditSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'login',
            'email',
            'avatar'
        ]


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

