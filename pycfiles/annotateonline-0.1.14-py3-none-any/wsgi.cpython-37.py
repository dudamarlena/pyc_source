# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/annotateme/standalone/wsgi.py
# Compiled at: 2018-11-12 05:32:24
# Size of source mod 2**32: 314 bytes
__doc__ = '\nWSGI config for annotateme project.\n\nIt exposes the WSGI callable as a module-level variable named ``application``.\n\nFor more information on this file, see\nhttps://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/\n'
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()