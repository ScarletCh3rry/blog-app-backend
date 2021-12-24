from django.contrib import admin
from .models import *


@admin.register(PostItem)
class PostItemAdmin(admin.ModelAdmin):
    readonly_fields = ('likes_count', 'comments_count', 'quizzes_count', 'views_count')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    readonly_fields = ('slug',)


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    readonly_fields = ('slug',)


@admin.register(UserPostRelation)
class UserPostRelationAdmin(admin.ModelAdmin):
    list_display = [
        'post',
        'user',
        'like',
        'watched'
    ]
