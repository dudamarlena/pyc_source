# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/narani/Projects/django-zen-queries/zen_queries/render.py
# Compiled at: 2020-03-13 12:34:20
# Size of source mod 2**32: 334 bytes
import django.shortcuts as django_render
from zen_queries import queries_disabled

def render(*args, **kwargs):
    """
    Wrapper around Django's `render` shortcut that is
    not allowed to run database queries
    """
    with queries_disabled():
        response = django_render(*args, **kwargs)
    return response