# Generated by Django 3.2.10 on 2022-06-13 17:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.CharField(default='', max_length=70, verbose_name='Ответ на вопрос')),
            ],
            options={
                'verbose_name': 'Ответ',
                'verbose_name_plural': 'Ответы',
            },
        ),
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, unique=True, verbose_name='Название блога')),
                ('description', models.CharField(max_length=1000, verbose_name='Описание блога')),
                ('slug', models.SlugField(verbose_name='Путь блога')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blogs', to=settings.AUTH_USER_MODEL, verbose_name='Владелец блога')),
            ],
            options={
                'verbose_name': 'Блог',
                'verbose_name_plural': 'Блоги',
                'unique_together': {('title', 'owner')},
            },
        ),
        migrations.CreateModel(
            name='PostItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, unique=True, verbose_name='Название поста')),
                ('description', models.TextField(verbose_name='Описание поста')),
                ('creation_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания поста')),
                ('likes_count', models.PositiveIntegerField(default=0, verbose_name='Количество лайков')),
                ('comments_count', models.PositiveIntegerField(default=0, verbose_name='Количество комментариев')),
                ('quizzes_count', models.PositiveIntegerField(default=0, verbose_name='Количество опросников')),
                ('views_count', models.PositiveIntegerField(default=0, verbose_name='Количество просмотров')),
                ('slug', models.SlugField(verbose_name='Путь поста')),
                ('blog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='blogs.blog', verbose_name='Блог')),
            ],
            options={
                'verbose_name': 'Пост',
                'verbose_name_plural': 'Посты',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25, unique=True, verbose_name='Имя тега')),
                ('slug', models.SlugField(unique=True, verbose_name='Путь')),
            ],
            options={
                'verbose_name': 'Тег поста',
                'verbose_name_plural': 'Теги постов',
            },
        ),
        migrations.CreateModel(
            name='UserPostRelation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('like', models.BooleanField(default=False)),
                ('watched', models.BooleanField(default=False)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blogs.postitem')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_relations', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Взаимодействие пользователя',
                'verbose_name_plural': 'Взаимодействия пользователя',
            },
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subscription_status', models.BooleanField(default=False, verbose_name='Подписан?')),
                ('user_who_subscribed', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscriptions', to=settings.AUTH_USER_MODEL, verbose_name='Тот кто подписалсля')),
                ('user_you_subscribed_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscribers', to=settings.AUTH_USER_MODEL, verbose_name='Тот на кого подписались')),
            ],
            options={
                'verbose_name': 'Подписка',
                'verbose_name_plural': 'Подписки',
            },
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=70, unique=True, verbose_name='Вопрос')),
                ('slug', models.SlugField(default='', unique=True, verbose_name='Путь опроса')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='blogs.postitem', verbose_name='Пост опроса')),
            ],
            options={
                'verbose_name': 'Опрос',
                'verbose_name_plural': 'Опросы',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=70, verbose_name='Вопрос')),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='blogs.quiz', verbose_name='Опрос вопроса')),
            ],
            options={
                'verbose_name': 'Вопрос',
                'verbose_name_plural': 'Вопросы',
            },
        ),
        migrations.AddField(
            model_name='postitem',
            name='tags',
            field=models.ManyToManyField(related_name='posts', to='blogs.Tag', verbose_name='Теги поста'),
        ),
        migrations.CreateModel(
            name='PassedQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='passed_questions', to='blogs.answer', verbose_name='Ответ')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='passed_question', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь который дал ответ')),
            ],
            options={
                'verbose_name': 'Пройденный вопрос',
                'verbose_name_plural': 'Пройденные вопросы',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=1000, verbose_name='Текст комментария')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL, verbose_name='Владелец комментария')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='blogs.postitem', verbose_name='Откомментированный пост')),
            ],
            options={
                'verbose_name': 'Комментарий',
                'verbose_name_plural': 'Комментарии',
            },
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='blogs.question', verbose_name='Вопрос ответа'),
        ),
        migrations.AlterUniqueTogether(
            name='postitem',
            unique_together={('title', 'blog')},
        ),
    ]