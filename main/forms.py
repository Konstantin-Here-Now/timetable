from django import forms
from .models import Lesson

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ('date_lesson', 'time_lesson', 'desc')
        widgets = {
            'date_lesson': forms.TextInput(attrs={'class': 'form-input', 'type': 'date'}),
            'time_lesson': forms.TimeInput(attrs={'class': 'form-input', 'type': 'time'}),
            'desc': forms.Textarea(attrs={'class': 'form-input'}),
        }


class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(min_length=3, max_length=30, label='Логин',
                               widget=forms.TextInput(attrs={'class': 'form-input'}))
    first_name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={'class': 'form-input'}))
    last_name = forms.CharField(label='Фамилия', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='Электронная почта', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Введите логин',
        widget=forms.TextInput(attrs={'class': 'form-input'}),
        min_length=2,
        max_length=30,
    )
    password = forms.CharField(
        label='Введите пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-input'}),
    )