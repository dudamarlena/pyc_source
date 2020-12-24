# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/chisubmit/backend/wsgi.py
# Compiled at: 2015-09-08 14:13:36
# Size of source mod 2**32: 401 bytes
__doc__ = '\nWSGI config for backend project.\n\nIt exposes the WSGI callable as a module-level variable named ``application``.\n\nFor more information on this file, see\nhttps://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/\n'
import os
from django.core.wsgi import get_wsgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chisubmit.backend.settings')
application = get_wsgi_application()