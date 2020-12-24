# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/kssworld93/Projects/appcubator-site/venv/lib/python2.7/site-packages/analytics/wsgi.py
# Compiled at: 2013-07-17 17:55:02
__doc__ = "\nWSGI config for analytics project.\n\nThis module contains the WSGI application used by Django's development server\nand any production WSGI deployments. It should expose a module-level variable\nnamed ``application``. Django's ``runserver`` and ``runfcgi`` commands discover\nthis application via the ``WSGI_APPLICATION`` setting.\n\nUsually you will have the standard Django WSGI application here, but it also\nmight make sense to replace the whole Django WSGI application with a custom one\nthat later delegates to the Django one. For example, you could introduce WSGI\nmiddleware here, or combine a Django application with an application of another\nframework.\n\n"
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'analytics.settings')
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()