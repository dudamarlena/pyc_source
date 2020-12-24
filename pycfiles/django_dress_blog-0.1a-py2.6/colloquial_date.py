# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dress_blog/templatetags/colloquial_date.py
# Compiled at: 2012-07-20 05:27:44
from django import template
from django.conf import settings
from dress_blog.utils import colloquial_date
register = template.Library()

@register.filter('colloquial_date', is_safe=False)
def colloquial_date_filter(value, arg=None):
    """
    Formats a date using colloquial words when within last week. 

    value - date or datetime
    arg   - date format in python or django date format
    
    Formats a date using colloquial words when within last week. 
    Otherwise uses settings.DATE_FORMAT
    """
    if not value:
        return ''
    else:
        if arg is None:
            arg = settings.DATE_FORMAT
        return colloquial_date(value, arg)