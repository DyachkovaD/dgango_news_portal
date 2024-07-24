from django.urls import path
from .views import PostDetail, ArticleCreate

urlpatterns = [
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('create/', ArticleCreate.as_view(), name='article_create')
]