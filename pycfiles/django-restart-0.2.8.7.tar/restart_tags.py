# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /var/projects/sr/sr/restart/templatetags/restart_tags.py
# Compiled at: 2015-03-26 05:58:42
from django import template
from django.template import defaultfilters
from django.utils.translation import pgettext, ungettext, ugettext as _
from classytags.core import Tag, Options
from classytags.arguments import Argument
from datetime import date, datetime
register = template.Library()

class RestartStatus(Tag):
    name = 'restart_status'

    def render_tag(self, context):
        status = True
        context['restart_status'] = status
        return ''


register.tag(RestartStatus)

@register.filter
def naturaltime(value):
    try:
        from django.contrib.humanize.templatetags.humanize import naturaltime as djangonaturaltime
        return djangonaturaltime(value)
    except:
        return '%s' % value