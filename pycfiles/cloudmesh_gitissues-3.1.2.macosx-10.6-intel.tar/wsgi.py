# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/big/ENV2/lib/python2.7/site-packages/cloudmesh_gitissues/wsgi.py
# Compiled at: 2016-03-14 09:31:39
"""
WSGI config for comet project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""
import os
from django.core.wsgi import get_wsgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cloudmesh_gitissues.settings')
application = get_wsgi_application()