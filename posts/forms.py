from django import forms
from .models import Post


class UserRegistrationForm(forms.Form):
    username = forms.CharField(
        required = True,
        label = 'Username',
        max_length = 32
    )
    email = forms.CharField(
        required = True,
        label = 'Email',
        max_length = 32,
    )
    password = forms.CharField(
        required = True,
        label = 'Password',
        max_length = 32,
        widget = forms.PasswordInput()
    )

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = (
            'title',
            'content',
            'post_image',
        )