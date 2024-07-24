from django import forms
from django.core.exceptions import ValidationError

from .models import Post


class PostForm(forms.ModelForm):
    text = forms.CharField(max_length=3000)

    class Meta:
        model = Post
        fields = ['title', 'author', 'category', 'text']