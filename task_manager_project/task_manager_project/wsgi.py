"""
WSGI config for task_manager_project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

import sys
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'task_manager_project.settings')

application = get_wsgi_application()



print("Current working directory:", os.getcwd())
print("sys.path:", sys.path)
