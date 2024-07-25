from django.shortcuts import render
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.urls import reverse, reverse_lazy

from datetime import datetime

from .models import Post
from .filters import PostFilter
from .forms import PostForm


class PostsList(ListView):
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


class PostCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        if self.request.path == '/posts/articles/create/':
            post.type = 'A'
        post.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('post_detail', args=(self.object.id,))


class PostUpdate(UpdateView):
    form_class = PostForm
    model = Post

    def get_template_names(self):
        if 'articles' in self.request.path and self.object.type == 'N'\
              or 'news' in self.request.path and self.object.type == 'A':
            return 'not_found.html'
        else:
            return 'post_edit.html'


class PostDelete(DeleteView):
    model = Post
    success_url = reverse_lazy('post_list')

    def get_template_names(self):
        if 'articles' in self.request.path and self.object.type == 'N' \
                or 'news' in self.request.path and self.object.type == 'A':
            return 'not_found.html'
        else:
            return 'post_delete.html'
