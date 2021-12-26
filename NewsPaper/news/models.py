from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        post_ratings = self.post_set.aggregate(post_values=Sum('rating'))
        posts_rating = 0
        posts_rating += post_ratings.get('post_values')

        comment_ratings = self.user.comment_set.aggregate(comment_values=Sum('rating'))
        comments_rating = 0
        comments_rating += comment_ratings.get('comment_values')

        self.rating = posts_rating * 3 + comments_rating
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ManyToManyField(Category, through='PostCategory')
    is_article = models.BooleanField(default=True)
    heading = models.CharField(max_length=128, default='Статья без названия')
    add_time = models.DateTimeField(auto_now_add=True)
    content = models.TextField(default='Статья без контента')
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        preview_content = str(self.content[0:123] + '...')
        return preview_content


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    text_add = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

