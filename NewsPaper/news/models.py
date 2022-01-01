from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0, verbose_name='Рейтинг')

    def update_rating(self):
        post_ratings = self.post_set.aggregate(post_values=Sum('rating'))
        posts_rating = 0
        posts_rating += post_ratings.get('post_values')

        comment_ratings = self.user.comment_set.aggregate(comment_values=Sum('rating'))
        comments_rating = 0
        comments_rating += comment_ratings.get('comment_values')

        self.rating = posts_rating * 3 + comments_rating
        self.save()

    def __str__(self):
        return '{}'.format(self.user.username)

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'


class Category(models.Model):
    name = models.CharField(max_length=128, unique=True, verbose_name='Наименование')

    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name='Автор')
    category = models.ManyToManyField(Category, through='PostCategory', verbose_name='Категория')
    is_article = models.BooleanField(default=True, verbose_name='Статья - да, Новость - нет')
    heading = models.CharField(max_length=128, default='Статья без названия', verbose_name='Заголовок')
    add_time = models.DateTimeField(auto_now_add=True)
    content = models.TextField(default='Статья без контента', verbose_name='Контент')
    rating = models.IntegerField(default=0, verbose_name='Рейтинг')

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        preview_content = str(self.content[0:123] + '...')
        return preview_content

    def __str__(self):
        return '{}'.format(f'{self.heading}: {self.content[0:20]} ...')

    class Meta:
        verbose_name = 'Публикация'
        verbose_name_plural = 'Публикации'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(verbose_name='Текст комментария')
    text_add = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def __str__(self):
        return '{}'.format(self.text[0:80])

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-text_add']

