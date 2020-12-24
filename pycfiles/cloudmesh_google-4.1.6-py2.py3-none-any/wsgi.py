# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/big/ENV2/lib/python2.7/site-packages/cloudmesh_gitissues/wsgi.py
# Compiled at: 2016-03-14 09:31:39
__doc__ = '\nWSGI config for comet project.\n\nIt exposes the WSGI callable as a module-level variable named ``application``.\n\nFor more information on this file, see\nhttps://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/\n'
import os
from django.core.wsgi import get_wsgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cloudmesh_gitissues.settings')
application = get_wsgi_application()