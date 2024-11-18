from .models import *
from rest_framework import serializers


class PostSerializer(serializers.ModelSerializer):
    # это, чтобы поле автор(юзер) в модели заполнялось автоматически, в зависимости от того, кто создал пост
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Post
        fields = ['id', 'title', 'type', 'author']