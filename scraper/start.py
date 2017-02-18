# celery worker -l info -A start --beat

from datetime import timedelta
from celery import Celery
from celery.task import periodic_task

import os

app = Celery('tasks', backend='amqp',
             broker='amqp://guest@localhost//')


@periodic_task(run_every=timedelta(hours=2))
def lost_pet():
    print "start"
    os.system("python celery_crawler.py")
    return;
