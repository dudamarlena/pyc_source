# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/omri/code/prediction/prediction/wsgi.py
# Compiled at: 2017-12-26 04:06:27
# Size of source mod 2**32: 409 bytes
__doc__ = '\nWSGI config for prediction project.\n\nIt exposes the WSGI callable as a module-level variable named ``application``.\n\nFor more information on this file, see\nhttps://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/\n'
import os
from django.core.wsgi import get_wsgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'prediction.settings.development')
application = get_wsgi_application()