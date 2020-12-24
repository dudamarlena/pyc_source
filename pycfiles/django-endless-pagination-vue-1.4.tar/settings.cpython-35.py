# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /media/martin/windows/Desarrollo/Python/django-endless-pagination-vue/bin/django-endless-pagination-vue/tests/endless_pagination/settings.py
# Compiled at: 2015-07-13 19:15:37
# Size of source mod 2**32: 2327 bytes
from __future__ import unicode_literals
from django.conf import settings
PER_PAGE = getattr(settings, 'ENDLESS_PAGINATION_PER_PAGE', 10)
PAGE_LABEL = getattr(settings, 'ENDLESS_PAGINATION_PAGE_LABEL', 'page')
ORPHANS = getattr(settings, 'ENDLESS_PAGINATION_ORPHANS', 0)
LOADING = getattr(settings, 'ENDLESS_PAGINATION_LOADING', 'loading')
PREVIOUS_LABEL = getattr(settings, 'ENDLESS_PAGINATION_PREVIOUS_LABEL', '&lt;')
NEXT_LABEL = getattr(settings, 'ENDLESS_PAGINATION_NEXT_LABEL', '&gt;')
FIRST_LABEL = getattr(settings, 'ENDLESS_PAGINATION_FIRST_LABEL', '&lt;&lt;')
LAST_LABEL = getattr(settings, 'ENDLESS_PAGINATION_LAST_LABEL', '&gt;&gt;')
ADD_NOFOLLOW = getattr(settings, 'ENDLESS_PAGINATION_ADD_NOFOLLOW', False)
PAGE_LIST_CALLABLE = getattr(settings, 'ENDLESS_PAGINATION_PAGE_LIST_CALLABLE', None)
DEFAULT_CALLABLE_EXTREMES = getattr(settings, 'ENDLESS_PAGINATION_DEFAULT_CALLABLE_EXTREMES', 3)
DEFAULT_CALLABLE_AROUNDS = getattr(settings, 'ENDLESS_PAGINATION_DEFAULT_CALLABLE_AROUNDS', 2)
DEFAULT_CALLABLE_ARROWS = getattr(settings, 'ENDLESS_PAGINATION_DEFAULT_CALLABLE_ARROWS', False)
TEMPLATE_VARNAME = getattr(settings, 'ENDLESS_PAGINATION_TEMPLATE_VARNAME', 'template')