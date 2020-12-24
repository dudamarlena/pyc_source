# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/announcements/templatetags/announcement_tags.py
# Compiled at: 2020-02-26 14:48:40
# Size of source mod 2**32: 657 bytes
from django.template import Library
from tendenci.apps.announcements.models import EmergencyAnnouncement
from tendenci.apps.perms.utils import get_query_filters
register = Library()

@register.inclusion_tag('announcements/emergency_area.html', takes_context=True)
def emergency_announcement(context, user):
    filters = get_query_filters(user, 'announcements.view_emergencyannouncement')
    announcements = EmergencyAnnouncement.objects.filter(filters).distinct()
    announcements = announcements.filter(enabled=True).order_by('-create_dt')
    context.update({'user':user, 
     'announcements':announcements})
    return context