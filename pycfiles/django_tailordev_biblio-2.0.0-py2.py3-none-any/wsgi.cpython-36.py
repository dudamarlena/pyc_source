# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/maupetit/projects/TailorDev/django-tailordev-biblio/sandbox/wsgi.py
# Compiled at: 2017-03-23 12:12:16
# Size of source mod 2**32: 381 bytes
"""
WSGI config for toto project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""
import os
from django.core.wsgi import get_wsgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
application = get_wsgi_application()