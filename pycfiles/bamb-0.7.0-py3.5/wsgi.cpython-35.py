# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/web/wsgi.py
# Compiled at: 2017-09-08 11:08:24
# Size of source mod 2**32: 513 bytes
"""
WSGI config for bamb project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""
import os
from os.path import dirname, abspath
import sys
from django.core.wsgi import get_wsgi_application
PROJECT_DIR = dirname(dirname(abspath(__file__)))
sys.path.insert(0, PROJECT_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web.settings')
application = get_wsgi_application()