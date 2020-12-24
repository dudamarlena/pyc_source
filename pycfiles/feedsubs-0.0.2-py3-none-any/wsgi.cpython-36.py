# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nicolas/dev/feedpubsub/feedsubs/wsgi.py
# Compiled at: 2018-10-06 14:28:24
# Size of source mod 2**32: 311 bytes
"""
WSGI config for feedsubs project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()