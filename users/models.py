from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import MinLengthValidator
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, email, login, password=None):
        if not email:
            raise ValueError('Email is required')
        if not login:
            raise ValueError('Login is required')
        user = self.model(
            email=self.normalize_email(email),
            login=login,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, login, password=None):

        user = self.create_user(
            email=email,
            login=login,
            password=password
        )
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.role = 'Admin'
        user.save(using=self._db)
        return user


ROLE_CHOICES = (
    ('User', 'User'),
    ('Moderator', 'Moderator'),
    ('Editor', 'Editor'),
    ('Admin', 'Admin')

)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    class Meta:
        verbose_name = 'Пользователя'
        verbose_name_plural = 'Пользователи'

    login = models.CharField(verbose_name="Логин", max_length=20, unique=True, validators=[MinLengthValidator(6)])
    email = models.EmailField(verbose_name="email", max_length=35, unique=True)
    last_login = models.DateTimeField(verbose_name="Последняя дата захода", auto_now=True)
    date_joined = models.DateTimeField(verbose_name="Дата регистрации", auto_now_add=True)
    role = models.CharField(verbose_name="Роль", choices=ROLE_CHOICES, max_length=15, default='User')
    is_active = models.BooleanField(default=False, verbose_name="Active",
                                    help_text='Определяет, следует ли считать этого пользователя активным. '
                                              'Снимите этот флажок вместо удаления учетных записей.')
    is_staff = models.BooleanField(default=False, verbose_name="Staff status",
                                   help_text='Определяет, может ли пользователь войти на этот сайт администратора.')
    is_superuser = models.BooleanField(default=False, verbose_name="Superuser status",
                                       help_text='Указывает, что у этого пользователя есть все '
                                                 'разрешения без их явного назначения.')
    avatar = models.ImageField(verbose_name='Аватар пользователя', default='default.jpg')

    USERNAME_FIELD = 'login'

    REQUIRED_FIELDS = ['email']

    objects = CustomUserManager()

    def __str__(self):
        return self.login
