# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/pierre/.virtualenvs/creativeloft/lib/python2.7/site-packages/responsive_admin/templatetags/responsive_style.py
# Compiled at: 2014-03-02 13:09:12
from django import template
from responsive_admin.conf import settings
register = template.Library()

def max_width():
    if settings.RESPONSIVE_ADMIN_CONTAINER_MAX_WIDTH != 0:
        style = '%ipx' % settings.RESPONSIVE_ADMIN_CONTAINER_MAX_WIDTH
        return style
    else:
        return 'none'


@register.inclusion_tag('templatetags/fixed_submit_line.html')
def fixed_submit_line():
    return {'FIXED_SUBMIT_LINE': settings.RESPONSIVE_ADMIN_FIXED_SUBMIT_LINE}


register.simple_tag(max_width)