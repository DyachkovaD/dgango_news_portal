from django.contrib import admin
from .models import Post, Category
from translation import *
from modeltranslation.admin import TranslationAdmin


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'type', 'rating', )
    list_filter = ('author', 'type', )


class CategoryAdmin(TranslationAdmin, admin.ModelAdmin):
    model = Category
    list_display = ('name', 'popularity', )
    list_filter = ('name', )


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
