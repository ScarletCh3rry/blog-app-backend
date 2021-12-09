from django.contrib.auth.models import User
from django.db import models, IntegrityError
from django.db.models import CASCADE
from django.utils.text import slugify

from users.models import CustomUser


class PostItem(models.Model):
    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    title = models.CharField(max_length=20, verbose_name='Название поста')
    description = models.TextField(verbose_name='Описание поста')
    tags = models.ManyToManyField('Tag', verbose_name='Теги поста', related_name='posts')
    creation_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания поста')
    likes_count = models.PositiveIntegerField(verbose_name='Количество лайков', default=0)
    comments_count = models.PositiveIntegerField(verbose_name='Количество комментариев', default=0)
    quizzes_count = models.PositiveIntegerField(verbose_name='Количество опросников', default=0)
    views_count = models.PositiveIntegerField(verbose_name='Количество просмотров', default=0)
    blog = models.ForeignKey('Blog', verbose_name='Блог', related_name='posts', on_delete=CASCADE)

    def __str__(self):
        return f'Пост: {self.title}'


class Tag(models.Model):
    class Meta:
        verbose_name = 'Тег поста'
        verbose_name_plural = 'Теги постов'

    name = models.CharField(max_length=20, verbose_name='Имя тега')
    slug = models.SlugField(verbose_name="Путь", unique=True)

    def __str__(self):
        return f'Тег: {self.name}'

    def save(self, *args, **kwargs):
        translated = self.name.translate(
            str.maketrans(
                "абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ",
                "abvgdeejzijklmnoprstufhzcss_y_euaABVGDEEJZIJKLMNOPRSTUFHZCSS_Y_EUA"
            ))
        self.slug = slugify(translated)
        super().save(*args, **kwargs)


class Blog(models.Model):
    class Meta:
        verbose_name = 'Блог'
        verbose_name_plural = 'Блоги'

    title = models.CharField(max_length=20, verbose_name='Название блога')
    owner = models.ForeignKey(CustomUser, verbose_name='Владелец блога', related_name='blogs', on_delete=CASCADE)

    def __str__(self):
        return f'Блог: {self.title}'
