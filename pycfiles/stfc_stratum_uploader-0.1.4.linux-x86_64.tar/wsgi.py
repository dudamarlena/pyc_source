# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/vwa13376/workspace/uploader/archer/wsgi.py
# Compiled at: 2013-08-08 06:21:34
"""
WSGI config for archer project.

This module contains the WSGI application used by Django's development server
and any production WSGI deployments. It should expose a module-level variable
named ``application``. Django's ``runserver`` and ``runfcgi`` commands discover
this application via the ``WSGI_APPLICATION`` setting.

Usually you will have the standard Django WSGI application here, but it also
might make sense to replace the whole Django WSGI application with a custom one
that later delegates to the Django one. For example, you could introduce WSGI
middleware here, or combine a Django application with an application of another
framework.

"""
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'archer.settings')
os.environ.setdefault('DJANGO_CONFIGURATION', 'Production')
from configurations.wsgi import get_wsgi_application
application = get_wsgi_application()
from django.contrib.auth.handlers.modwsgi import check_password