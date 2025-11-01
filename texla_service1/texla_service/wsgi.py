"""
WSGI config for texla_service project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'texla_service1.texla_service.settings')
print(">>> Current working directory:", os.getcwd())
print(">>> Contents:", os.listdir(os.getcwd()))

application = get_wsgi_application()
