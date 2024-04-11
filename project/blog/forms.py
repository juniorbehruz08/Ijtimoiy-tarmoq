from django import forms
from .models import *
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = [
            'title',
            'content',
            'photo',
            'category'
        ]

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control rounded',
                'placeholder': 'Article title'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control rounded',
                'placeholder': 'Article content'
            }),
            'photo': forms.FileInput(attrs={
                'class': 'form-control rounded'
            }),
            'category': forms.Select(attrs={
                'class': 'form-control rounded'
            })
        }


class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=16, help_text='Maximum 16 Character',
                               widget=forms.TextInput(attrs={
                                   'class': 'form-control rounded',
                                   'placeholder': 'Username'
                               }))
    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput(attrs={
                                   'class': 'form-control rounded',
                                   'placeholder': 'Password'
                               })
                               )


class RegistrationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control rounded',
        'name': 'username',
        'placeholder': 'Username ( Iloji boricha son va belgilardan foydalaning )'
    }))
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control rounded',
        'placeholder': 'First Name ( Belgilar va sonlarni ishlatmang!!! )'
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control rounded',
        'placeholder': 'Last Name ( Belgilar va sonlarni ishlatmang!!! )'
    }))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'form-control rounded',
        'placeholder': 'Email'
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control rounded',
        'placeholder': 'Password ( Kamida 8 ta belgi harflar, sonlar va belgilardan qatnashtirish talab etiladi )'
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control rounded',
        'placeholder': 'Return Password ( Parolni takrorlang )'
    }))

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2'
        )


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = (
            'comment',
        )

    comment = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': "Your Comment"
    }))


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = (
            'message',
        )

    message = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control rounded',
        'placeholder': 'Your message'
    }))


class PhotoForm(forms.ModelForm):
    class Meta:
        model = AccountPhoto
        fields = (
            'photo',
        )

    photo = forms.FileField(widget=forms.FileInput(attrs={
        'class': 'form-control'
    }))
