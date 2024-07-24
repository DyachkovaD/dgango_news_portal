import django_filters
from django import forms
from django_filters import FilterSet
from .models import Post


class PostFilter(FilterSet):
    date = django_filters.DateFilter(
        field_name='date',
        label='Date of publication',
        lookup_expr='lt',
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = Post
        fields = {
            'title': ['icontains'],
            'author__user': ['exact'],
        }