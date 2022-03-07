from celery import shared_task

from celery import shared_task
import time

@shared_task
def hello():
    time.sleep(10)
    print("Hello, world!")