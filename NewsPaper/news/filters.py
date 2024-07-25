import django_filters
from django import forms
from django_filters import FilterSet
from .models import Post


class PostFilter(FilterSet):
    title = django_filters.CharFilter(
        field_name='title',
        label='Title',
        lookup_expr='iregex'
    )
    author = django_filters.CharFilter(
        field_name='author__user__username',
        label='Author',
        lookup_expr='exact'
    )
    date = django_filters.DateFilter(
        field_name='date',
        label='Date of publication',
        lookup_expr='lt',
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = Post
        fields = ('title', 'author', 'date')