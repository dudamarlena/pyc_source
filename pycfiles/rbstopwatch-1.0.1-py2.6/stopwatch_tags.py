# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-intel/egg/rbstopwatch/templatetags/stopwatch_tags.py
# Compiled at: 2015-11-30 19:18:58
from __future__ import division, unicode_literals
from django import template
from django.utils.html import format_html
from django.utils.translation import ugettext as _
register = template.Library()

@register.filter
def review_time(review):
    if review.extra_data and b'rbstopwatch.reviewTime' in review.extra_data:
        totalSeconds = int(review.extra_data[b'rbstopwatch.reviewTime'])
        hours = totalSeconds // 3600
        minutes = totalSeconds % 3600 // 60
        seconds = totalSeconds % 60
        time = b'%02d:%02d:%02d' % (hours, minutes, seconds)
        return format_html(b'<div class="rbstopwatch-review-header">{0}</div>', _(b'Total time spent on this review: %s') % time)
    return b''