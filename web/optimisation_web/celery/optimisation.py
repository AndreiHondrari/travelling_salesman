"""
Celery app to interact with the optimisation service worker remotely
"""
import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'optimisation_web.settings')

optimisation_celery_app = Celery()
optimisation_celery_app.config_from_object('django.conf:settings', namespace='CELERY_OPTIMISATION')
