from django import forms
from django.core.exceptions import ValidationError
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group

from datetime import datetime

from .models import Post


class PostForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.action = kwargs.pop('action')
        super().__init__(*args, **kwargs)

    text = forms.CharField(max_length=3000)

    class Meta:
        model = Post
        fields = ['title', 'author', 'category', 'text']

    def clean(self):
        cleaned_data = super(PostForm, self).clean()
        author = cleaned_data.get('author')
        posts_today = len(Post.objects.filter(author=author, date__day=datetime.today().day))
        if self.action == 'create' and posts_today >= 3:
            raise ValidationError("Вы не можете создавать более трёх постов в день.")
        else:
            return cleaned_data


class BasicSignupForm(SignupForm):
    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return user