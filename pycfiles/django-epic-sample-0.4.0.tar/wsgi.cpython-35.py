# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /data1/home/davidm/egauge/django-epic-sample/epic-sample/epic-sample/wsgi.py
# Compiled at: 2015-09-01 17:49:32
# Size of source mod 2**32: 395 bytes
"""
WSGI config for tstproject project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tstproject.settings')
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()