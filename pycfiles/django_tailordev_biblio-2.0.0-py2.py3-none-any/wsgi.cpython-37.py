# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/maupetit/projects/TailorDev/django-tailordev-biblio/sandbox/wsgi.py
# Compiled at: 2018-11-13 15:51:41
# Size of source mod 2**32: 212 bytes
"""
WSGI config for td_biblio sandbox.
"""
import os
from django.core.wsgi import get_wsgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sandbox.settings')
application = get_wsgi_application()