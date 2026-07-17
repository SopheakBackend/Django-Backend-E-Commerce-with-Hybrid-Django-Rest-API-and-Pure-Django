import os #os is the django variable(we can talk to django itselft using os)
from celery import Celery

#this: tells Celery what setting to use(django settings itself)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myshop.settings')

#this: Create Celery application instance, so we might call it later
app = Celery('myshop')

#this: tells Celery to use any code block or line that start with Celery_ in settings.py
app.config_from_object('django.conf:settings', namespace='CELERY')

#this: tell celery to auto pick up any task from all application, if there is any
app.autodiscover_tasks()