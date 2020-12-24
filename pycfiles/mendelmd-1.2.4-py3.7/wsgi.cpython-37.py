# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mendelmd/wsgi.py
# Compiled at: 2019-05-07 08:43:55
# Size of source mod 2**32: 784 bytes
"""
WSGI config for mendelmd project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""
import os, site, sys
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mendelmd.settings')
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()