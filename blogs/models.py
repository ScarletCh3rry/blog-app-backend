from django.contrib.auth.models import User
from django.db import models, IntegrityError
from django.db.models import CASCADE
from django.utils.text import slugify

from blogs.utils import use_slugify
from users.models import CustomUser


class PostItem(models.Model):
    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        unique_together = ('title', 'blog')

    title = models.CharField(max_length=20, verbose_name='Название поста')
    description = models.TextField(verbose_name='Описание поста')
    tags = models.ManyToManyField('Tag', verbose_name='Теги поста', related_name='posts')
    creation_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания поста')
    likes_count = models.PositiveIntegerField(verbose_name='Количество лайков', default=0)
    comments_count = models.PositiveIntegerField(verbose_name='Количество комментариев', default=0)
    quizzes_count = models.PositiveIntegerField(verbose_name='Количество опросников', default=0)
    views_count = models.PositiveIntegerField(verbose_name='Количество просмотров', default=0)
    blog = models.ForeignKey('Blog', verbose_name='Блог', related_name='posts', on_delete=CASCADE)
    slug = models.SlugField(verbose_name='Путь поста')

    def __str__(self):
        return f'Пост: {self.title}'

    def save(self, *args, **kwargs):
        self.slug = use_slugify(self.title)
        super().save(*args, **kwargs)


class UserPostRelation(models.Model):
    class Meta:
        verbose_name = 'Взаимодействие пользователя'
        verbose_name_plural = 'Взаимодействия пользователя'

    post = models.ForeignKey(PostItem, on_delete=CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=CASCADE, related_name='post_relations')
    like = models.BooleanField(default=False)
    watched = models.BooleanField(default=False)


class Tag(models.Model):
    class Meta:
        verbose_name = 'Тег поста'
        verbose_name_plural = 'Теги постов'

    name = models.CharField(max_length=20, verbose_name='Имя тега')
    slug = models.SlugField(verbose_name="Путь", unique=True)

    def __str__(self):
        return f'Тег: {self.name}'

    def save(self, *args, **kwargs):
        self.slug = use_slugify(self.name)
        super().save(*args, **kwargs)


class Blog(models.Model):
    class Meta:
        verbose_name = 'Блог'
        verbose_name_plural = 'Блоги'
        unique_together = ('title', 'owner')

    title = models.CharField(max_length=20, verbose_name='Название блога')
    description = models.CharField(max_length=400, verbose_name='Описание блога')
    owner = models.ForeignKey(CustomUser, verbose_name='Владелец блога', related_name='blogs', on_delete=CASCADE)
    slug = models.SlugField(verbose_name='Путь блога')

    def __str__(self):
        return f'Блог: {self.title}'

    def save(self, *args, **kwargs):
        self.slug = use_slugify(self.title)
        super().save(*args, **kwargs)


class Comment(models.Model):
    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    text = models.CharField(max_length=1000, verbose_name='Текст комментария')
    owner = models.ForeignKey(CustomUser, verbose_name='Владелец комментария', related_name='comments',
                              on_delete=CASCADE)
    post = models.ForeignKey(PostItem, verbose_name='Откомментированный пост', related_name='comments',
                             on_delete=CASCADE)

# class Quiz(models.Model):
#     class Meta:
#         verbose_name = 'Комментарий'
#         verbose_name_plural = 'Комментарии'
#
#     post = models.ForeignKey(PostItem, verbose_name='Откомментированный пост', related_name='comments',
#                              on_delete=CASCADE)
