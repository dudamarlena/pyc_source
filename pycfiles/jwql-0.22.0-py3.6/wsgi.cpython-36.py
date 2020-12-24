# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/jwql/website/jwql_proj/wsgi.py
# Compiled at: 2019-08-26 11:08:03
# Size of source mod 2**32: 517 bytes
"""WSGI config for ``jwql`` project.

It exposes the WSGI callable as a module-level variable named
``application``.

References
----------

    For more information on this file, see:
        ``https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/``
"""
import os
from django.core.wsgi import get_wsgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jwql.website.jwql_proj.settings')
application = get_wsgi_application()