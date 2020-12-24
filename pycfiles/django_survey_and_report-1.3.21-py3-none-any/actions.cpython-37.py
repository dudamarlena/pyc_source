# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pierre/workspace/django-survey/survey/actions.py
# Compiled at: 2020-02-23 10:00:28
# Size of source mod 2**32: 603 bytes
import django.utils.translation as _
from django.utils.translation import ungettext

def make_published(modeladmin, request, queryset):
    """
    Mark the given survey as published
    """
    count = queryset.update(is_published=True)
    message = ungettext('%(count)d survey was successfully marked as published.', '%(count)d surveys were successfully marked as published', count) % {'count': count}
    modeladmin.message_user(request, message)


make_published.short_description = _('Mark selected surveys as published')