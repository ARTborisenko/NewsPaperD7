from django.views.generic import TemplateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User, Group
from .forms import UserForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives, mail_admins
from django.template.loader import render_to_string


class AuthorUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'protect/author_create.html'
    form_class = UserForm
    queryset = User.objects.all()
    success_url = '/news/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        return context


@login_required
def upgrade_me(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')

    html_content = render_to_string(
        'protect/mail.html',
        {
            'user': request.user
        }
    )

    msg = EmailMultiAlternatives(
        subject=f'{request.user} стал автором!',
        body='На нашем сайте новый автор, познакомьтесь с ним!',
        from_email='TemaB1og@yandex.ru',
        to=['artyom2580456@mail.ru'],
    )
    msg.attach_alternative(html_content, 'text/html')

    msg.send()

    mail_admins(
        subject='Тема письма',
        message='Текст письма, который приходит всем администраторам'
    )

    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)

    return redirect('/news/')