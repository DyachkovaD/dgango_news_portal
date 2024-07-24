from django.urls import path
from .views import PostsList, PostDetail, FilterList, NewsCreate

urlpatterns = [
    path('', PostsList.as_view(), name='post_list'),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('search/', FilterList.as_view(), name='post_filter'),
    path('create/', NewsCreate.as_view(), name='news_create')
]