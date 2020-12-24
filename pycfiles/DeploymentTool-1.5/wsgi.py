# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\FilePkl\hasil_development\Deployment\Deployment\Deployment\wsgi.py
# Compiled at: 2014-09-29 02:22:40
"""
WSGI config for Deployment project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Deployment.settings')
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()