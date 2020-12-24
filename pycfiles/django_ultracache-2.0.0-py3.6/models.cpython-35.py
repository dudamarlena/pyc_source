# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hedley/django/instances/django-ultracache/ultracache/models.py
# Compiled at: 2018-09-10 07:18:29
# Size of source mod 2**32: 572 bytes
from django.conf import settings
try:
    tcp = settings.TEMPLATES[0]['OPTIONS']['context_processors']
except (AttributeError, KeyError):
    try:
        tcp = settings.TEMPLATE_CONTEXT_PROCESSORS
    except AttributeError:
        tcp = []

if 'django.core.context_processors.request' not in tcp and 'django.template.context_processors.request' not in tcp:
    raise RuntimeError('django.template.context_processors.request is required')
import ultracache.monkey