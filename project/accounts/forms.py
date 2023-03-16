from django import forms
from allauth.account.forms import SignupForm
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm
from django.template.loader import render_to_string
from django.core.mail import (
    EmailMultiAlternatives, send_mail, mail_managers, mail_admins
)


class CustomSignupForm(SignupForm):
    def save(self, request):
        user = super().save(request)
        reg_group_users = Group.objects.get(name="users")
        user.groups.add(reg_group_users)

        # Отправить обычное письмо зарегистрированному пользователю
        # send_mail(
        #     subject='Добро пожаловать в наш интернет-магазин!',
        #     message=f'{user.username}, вы успешно зарегистрировались!',
        #     from_email=None,
        #     recipient_list=[user.email],
        # )

        # Отправить "text/html" письмо зарегистрированному пользователю
        subject = 'Добро пожаловать в наш интернет-магазин!'
        text = f'{user.username}, вы успешно зарегистрировались на сайте!'
        html = render_to_string('registration/reg_greet.html',
                                context={'username': user.username})
        msg = EmailMultiAlternatives(
            subject=subject, body=text, from_email=None, to=[user.email]
        )
        msg.attach_alternative(html, 'text/html')
        msg.send()

        # Отправить сообщение всем менеджерам о новом пользователе
        # mail_managers(
        #     subject='Новый пользователь!',
        #     message=f'Пользователь "{user.username}" {user.email} '
        #             f'- зарегистрировался на сайте.'
        # )

        # Отправить сообщение всем администраторам о новом пользователе
        # mail_admins(
        #     subject='Новый пользователь!',
        #     message=f'Пользователь "{user.username}" {user.email} '
        #             f'- зарегистрировался на сайте.',
        #     html_message=None
        # )

        return user


class SignUpForm(UserCreationForm):
    username = forms.CharField(label="Ник")
    first_name = forms.CharField(label="Имя")
    last_name = forms.CharField(label="Фамилия")
    email = forms.EmailField(label="Email")
    password1 = forms.CharField(label="Пароль")
    password2 = forms.CharField(label="Повторить пароль")

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        )
