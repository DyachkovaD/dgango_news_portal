from django.urls import path
from .views import \
    (PostsList, PostDetail, PostCreate, PostUpdate, PostDelete, CategoryList, subscribe, unsubscribe)

urlpatterns = [
    path('', PostsList.as_view(), name='post_list'),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('search/', PostsList.as_view(), name='post_filter'),
    path('news/create/', PostCreate.as_view(), name='news_create'),
    path('articles/create/', PostCreate.as_view(), name='article_create'),
    path('news/<int:pk>/edit', PostUpdate.as_view(), name='news_update'),
    path('articles/<int:pk>/edit', PostUpdate.as_view(), name='articles_update'),
    path('news/<int:pk>/delete', PostDelete.as_view(), name='news_delete'),
    path('articles/<int:pk>/delete', PostDelete.as_view(), name='articles_delete'),
    path('category/<int:pk>', CategoryList.as_view(), name='category_list'),
    path('category/<int:pk>', subscribe, name='subscribe'),
    path('category/<int:pk>', unsubscribe, name='unsubscribe'),
]