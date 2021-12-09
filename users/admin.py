from django import forms
from django.contrib import admin

# Register your models here.
from users.models import CustomUser
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class CustomUserCreationForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = CustomUser
        fields = ('email',)


class CustomUserChangeForm(UserChangeForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = CustomUser
        fields = '__all__'


class UserAdmin(BaseUserAdmin):
    ordering = ['login']
    list_display = ['login', 'is_active', 'role']
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    readonly_fields = ['last_login', 'date_joined']
    fieldsets = (
        ('Персональные данные', {'fields': ('login', 'email', 'password', 'role')}),
        ('Права', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Важные даты', {'fields': ('last_login', 'date_joined')})

    )
    add_fieldsets = (
        (None, {
            'fields': ('avatar', 'login', 'email', 'password1', 'password2')}
         ),
    )
    search_fields = ["login"]


admin.site.register(CustomUser, UserAdmin)