
from __future__ import absolute_import
import logging
import os
from celery import Celery
from django.apps import AppConfig
from django.conf import settings


if not settings.configured:
    # set the default Django settings module for the 'celery' program.
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')  # pragma: no cover

from celery.utils.log import get_task_logger

logger = logging.getLogger("django")

app_celery = Celery('boe_api',
                    backend=settings.CELERY_RESULT_BACKEND,
                    broker=settings.BROKER_URL,
                    include=[
                        'boe_api.state_documents.tasks',
                    ])

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app_celery.config_from_object('django.conf:settings')
app_celery.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app_celery.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


app_celery.conf.update(
    CELERY_RESULT_BACKEND=settings.CELERY_RESULT_BACKEND,
    CELERY_TASK_RESULT_EXPIRES=settings.CELERY_TASK_RESULT_EXPIRES,
)


def get_task_status(cls_celery, task_id):
    task = cls_celery.AsyncResult(task_id)

    status = task.status
    progress = 0

    if status == u'SUCCESS':
        progress = 100
    elif status == u'FAILURE':
        progress = 0
    elif status == u'PROGRESS':
        progress = task.info['progress']

    return {'status': status, 'progress': progress}


if __name__ == '__main__':
    app_celery.start()
