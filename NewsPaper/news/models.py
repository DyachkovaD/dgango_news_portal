from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.urls import reverse


from django.core.validators import MinValueValidator


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        posts_rating = self.post_set.aggregate(pr=Coalesce(Sum('rating'), 0))['pr']
        comments_rating = self.user.comment_set.aggregate(cr=Coalesce(Sum('rating'), 0))['cr']
        post_comments_rating = self.post_set.aggregate(pcr=Coalesce(Sum('comment__rating'), 0))['pcr']

        self.rating = posts_rating + comments_rating * 3 + post_comments_rating
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    subscribers = models.ManyToManyField(User, through='UserCategory', related_name='categories', blank=True)

    def __str__(self):
        return self.name.title()


class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

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

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    type = models.CharField(max_length=1, choices=POSITIONS, default=news)
    date = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(
        Category,
        through='PostCategory',
        related_name='posts',)
    title = models.CharField(max_length=225)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.author.user}: {self.title}'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[:124] + ' ...'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class UserCategory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
