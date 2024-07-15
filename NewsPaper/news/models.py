from django.db import models
from django.contrib.auth.models import User
from functools import reduce



class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)  # !!!!!

    # def update_rating(self):
    #     posts_rating = self.post_set.all().values('rating')
    #     posts_rating_sum = reduce(lambda x, y: x + y, map(lambda x: x.get('pk'), posts_rating)) * 3
    #





class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)


class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)  # !!!!!

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()


class Post(models.Model):
    article = 'A'
    news = 'N'
    POSITIONS = [
        (article, 'статья'),
        (news, 'новость')
    ]

    author = models.ForeignKey('Author', on_delete=models.CASCADE)
    type = models.CharField(max_length=1, choices=POSITIONS, default=news)
    date = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField('Category', through='PostCategory')
    title = models.CharField(max_length=225)
    text = models.TextField()
    rating = models.IntegerField(default=0)  # !!!!

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[:124] + ' ...'


class PostCategory(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)

