# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/base/templatetags/reports_tags.py
# Compiled at: 2020-02-26 14:48:40
# Size of source mod 2**32: 1327 bytes
from builtins import str
from datetime import datetime
from django import template
import django.utils.translation as _
register = template.Library()

class MonthUrlNode(template.Node):

    def __init__(self, kind):
        self.kind = kind

    def render(self, context):
        request = context['request']
        now = datetime.now()
        year = int(request.GET.get('year') or str(now.year))
        month = int(request.GET.get('month') or str(now.month))
        year, month = self._move(year, month)
        query = request.GET.copy()
        query['month'] = month
        query['year'] = year
        return query.urlencode()

    def _move(self, year, month):
        if self.kind == 'previous':
            month -= 1
            if month < 1:
                month = 12
                year -= 1
        elif self.kind == 'next':
            month += 1
            if month > 12:
                month = 1
                year += 1
        return (
         year, month)


@register.tag
def month_url(parser, token):
    try:
        tag, kind = token.contents.split()
        if kind not in ('next', 'previous'):
            raise ValueError('Not next/previous')
    except ValueError:
        raise template.TemplateSyntaxError(_('Usage {% month_url next|previous %}'))

    return MonthUrlNode(kind)