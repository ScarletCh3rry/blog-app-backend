# Generated by Django 3.2.10 on 2021-12-24 06:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0003_blog_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='slug',
            field=models.SlugField(default='qweeqweq', verbose_name='Путь блога'),
            preserve_default=False,
        ),
    ]
