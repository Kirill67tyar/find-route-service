from django.contrib.auth.hashers import check_password
from django.contrib.auth import get_user_model, authenticate
from django.forms import (
    Form, CharField, PasswordInput, TextInput, ValidationError
)

from accounts.utils import get_object_or_null

User = get_user_model()


class LoginForm(Form):
    username = CharField(label='Логин',
                         required=True,
                         widget=TextInput(attrs={
                             'class': '',
                             'placeholder': 'Введите логин'
                         }))
    password = CharField(label='Пароль',
                         required=True,
                         widget=PasswordInput(attrs={
                             'class': 'form-control',
                             'placeholder': 'Введите пароль',
                         }))

    def clean(self, *args, **kwargs):
        data = self.cleaned_data
        username = data.get('username')
        password = data.get('password')
        if username and password:
            user = get_object_or_null(model=User, username=username)

            if not user:
                raise ValidationError('Пользователя с таким логином не существует')
            if not check_password(password, user.password):
                raise ValidationError('Пароль неправильный')
            user = authenticate(username=username, password=password)
            if not user:
                raise ValidationError('Данный аккаунт был заблокирован')
        return super().clean(*args, **kwargs)
