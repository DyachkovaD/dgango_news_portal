"""
URL configuration for NewsPaper project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from news import views

router = routers.DefaultRouter()
router.register(r'news', views.NewsViewset, basename='news')
router.register(r'articles', views.ArticlesViewset, basename='articles')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('pages/', include('django.contrib.flatpages.urls')),
    path('posts/', include('news.urls')),
    path('accounts/', include('allauth.urls')),
    path('', include('protect.urls')),
    path('sign/', include('sign.urls')),
    path('i18n/', include('django.conf.urls.i18n')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/v1/', include(router.urls))
]