from __future__ import absolute_import , unicode_literals
import os
from celery import Celery 


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'VideoSearch.settings')

app = Celery('VideoSearch')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.discover_tasks()