from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin

from datetime import datetime

from .models import Post, Category, UserCategory, PostCategory
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


class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post')

    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        if self.request.path == '/posts/articles/create/':
            post.type = 'A'
        post.save()

        return super().form_valid(form)


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


@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    if user not in category.subscribers.all():
        category.subscribers.add(user)
        message = 'Вы подписались на рассылку новостей категории'
    else:
        category.subscribers.remove(user)
        message = 'Вы отписались от рассылки новостей категории'
    return render(request, 'subscribe.html', {'category': category, 'message': message})




