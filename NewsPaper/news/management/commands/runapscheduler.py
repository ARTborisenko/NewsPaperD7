import logging
from django.conf import settings
import datetime

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from ...models import Post, Category

logger = logging.getLogger(__name__)


def my_job():
    all_category_pk = []
    subs_cat_email = {}
    date_now = datetime.datetime.now()
    week = datetime.timedelta(days=7)
    date_a_week_ago = date_now - week
    list = {}
    email_list = []
    for category in Category.objects.all():
        all_category_pk.append(category.pk)
    for pk in all_category_pk:
        for user in Category.objects.get(pk=pk).subscribers.all():
            if user.email not in subs_cat_email.keys():
                subs_cat_email[user.email] = [pk]
            else:
                subs_cat_email[user.email].append(pk)
    print(subs_cat_email)
    for post in Post.objects.filter(add_time__gte=date_a_week_ago):
        for category in post.category.all():
            cat_pk = category.pk
            if cat_pk not in list.keys():
                list[cat_pk] = [post.pk]
            else:
                list[cat_pk].append(post.pk)
    print(list)


# функция, которая будет удалять неактуальные задачи
def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # добавляем работу нашему задачнику
        scheduler.add_job(
            my_job,
            trigger=CronTrigger(second="*/3"),
            # То же, что и интервал, но задача тригера таким образом более понятна django
            id="my_job",  # уникальный айди
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            # Каждую неделю будут удаляться старые задачи, которые либо не удалось выполнить,
            # либо уже выполнять не надо.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
