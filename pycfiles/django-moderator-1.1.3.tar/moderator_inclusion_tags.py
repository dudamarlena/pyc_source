# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tonym/work/django-moderator/moderator/templatetags/moderator_inclusion_tags.py
# Compiled at: 2013-11-20 10:33:06
from django import template
register = template.Library()

@register.inclusion_tag('moderator/inclusion_tags/report_comment_abuse.html', takes_context=True)
def report_comment_abuse(context, obj):
    """
    Checks whether a user can report abuse (has not liked comment previously)
    or has reported abuse previously and renders appropriate response.

    If requesting user is part of the 'Moderators' group a vote equal to
    ABUSE_CUTOFF setting will be made, thereby immediately marking the comment
    as abusive.
    """
    context.update({'content_obj': obj, 
       'vote': -1, 
       'content_type': ('-').join((obj._meta.app_label, obj._meta.module_name))})
    return context