from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView, View
)
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.cache import cache
from rest_framework import viewsets
from rest_framework import permissions

from datetime import datetime

from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Post, Category
from .filters import PostFilter
from .forms import PostForm
from .serializers import *


class Time(View):
    def post(self, request):
        request.session['django_timezone'] = request.POST['timezone']
        return redirect(request.META['HTTP_REFERER'])  # перенаправление на текущую страницу (просто обнавление страницы)


class PostsList(ListView):
    #. Translators: This message appears on the home page only
    model = Post
    ordering = '-date'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        context['time_now'] = datetime.utcnow()
        return context

    def get_template_names(self):
        if self.request.path == '/posts/search/':
            return 'search.html'
        return 'posts.html'


class PostDetail(DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post'

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'post-{self.kwargs["pk"]}', None)
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post-{self.kwargs["pk"]}', obj)
        return obj


class PostCreate(PermissionRequiredMixin, CreateView):

    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        if self.request.path == '/posts/articles/create/':
            post.type = 'A'
        post.save()

        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'action': 'create'})
        return kwargs


class PostUpdate(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = ('news.change_post')

    form_class = PostForm
    model = Post

    def get_template_names(self):
        if 'articles' in self.request.path and self.object.type == 'N'\
              or 'news' in self.request.path and self.object.type == 'A':
            return 'not_found.html'
        else:
            return 'post_edit.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'action': 'update'})
        return kwargs


class PostDelete(DeleteView):
    model = Post
    success_url = reverse_lazy('post_list')

    def get_template_names(self):
        if 'articles' in self.request.path and self.object.type == 'N' \
                or 'news' in self.request.path and self.object.type == 'A':
            return 'not_found.html'
        else:
            return 'post_delete.html'


class CategoryList(ListView):
    model = Post
    template_name = 'category_list.html'
    context_object_name = 'category_post_list'
    paginate_by = 10

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(category=self.category).order_by('-date')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
        context['category'] = self.category
        return context


class NewsViewset(viewsets.ModelViewSet):
    queryset = Post.objects.filter(type='N')
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class ArticlesViewset(viewsets.ModelViewSet):
    queryset = Post.objects.filter(type='A')
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)
    return redirect('category_list', pk)


@login_required
def unsubscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.remove(user)
    return redirect('category_list', pk)

