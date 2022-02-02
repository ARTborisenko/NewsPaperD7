from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Post, Category
from django.db.models.signals import m2m_changed
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.auth.models import User

#Не придумал как сделать разделение на созданный и измененный пост.
#Знаю, что если человек подписан на 2 категории - то он получит 2 письма.
#Не сделал, т.к. не хватает времени, уже третью неделю модуль делаю...

@receiver(post_save, sender=Post.category.through)
def notify_subscribers(sender, instance, **kwargs):
    post = Post.objects.get(pk=instance.pk)
    categorys = post.category.all()
    for c in categorys:
        html_content = render_to_string(
            'news/post_created.html',
            {
                'heading': post.heading[:30],
                'content': post.content[:30],
                'post_pk': post.pk
            }
        )
        emails = []
        for user in Category.objects.get(pk=c.pk).subscribers.all():
            emails.append(user.email)
        msg = EmailMultiAlternatives(
            subject=f"В категории {Category.objects.get(pk=c.pk)} новая статья!!!",
            body=f"Взгляните!: \n",
            from_email='TemaB1og@yandex.ru',
            to=emails
        )

        msg.attach_alternative(html_content, "text/html")

        msg.send()

@receiver(post_save, sender=User)
def hi_user(sender, instance, created, **kwargs):
    if created:
        html_content = render_to_string(
            'account/email/new_user.html',
            {
                'user': instance.username,
            }
        )
        msg = EmailMultiAlternatives(
            subject=f"Привет!",
            body=f"Добро пожаловать!",
            from_email='TemaB1og@yandex.ru',
            to=[instance.email,]
        )

        msg.attach_alternative(html_content, "text/html")

        msg.send()

m2m_changed.connect(notify_subscribers, sender=Post.category.through)

