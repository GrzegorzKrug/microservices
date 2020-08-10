from __future__ import absolute_import, unicode_literals
from celery import Celery
import os

user = os.getenv('LOGIN', 'admin')
password = os.getenv('PASSWORD', 'mypass')
hostname = os.getenv('HOSTNAME', 'localhost')
port = os.getenv('PORT', '5673')

broker_url = f'amqp://{user}:{password}@{hostname}:{port}'
app = Celery("tasks", broker=broker_url, namespace="image_celery", include=['image_collector.tasks'])

__all__ = ("app",)
