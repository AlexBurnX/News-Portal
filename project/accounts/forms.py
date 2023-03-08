from django import forms
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CustomSignupForm(SignupForm):
    def save(self, request):
        user = super().save(request)
        reg_group_users = Group.objects.get(name="users")
        user.groups.add(reg_group_users)

        # authors = Group.objects.get(name='authors')
        # perm = Permission.objects.get(name='Can add post')
        # authors.permissions.add(perm)
        # perm = Permission.objects.get(name='Can change post')
        # authors.permissions.change(perm)
        # perm = Permission.objects.get(name='Can delete post')
        # authors.permissions.delete(perm)

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
