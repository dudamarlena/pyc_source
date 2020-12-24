# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/gustavofonseca/prj/github/scielo-django-extensions/scielo_extensions/context_processors.py
# Compiled at: 2012-03-21 14:31:07
from django.conf import settings

def from_settings(request):
    """
    Provides certain settings in the templates.

    Searches for an associative list named AVAILABLE_IN_TEMPLATES
    in settings.py.
    """
    try:
        return dict(settings.AVAILABLE_IN_TEMPLATES)
    except (ValueError, AttributeError):
        return {}