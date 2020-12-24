# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/wlfilebrowser/templatetags/fb_pagination.py
# Compiled at: 2016-04-17 01:57:03
from __future__ import unicode_literals
from future.builtins import range
from django.template import Library
register = Library()
DOT = b'.'

@register.inclusion_tag(b'wlfilebrowser/include/paginator.html', takes_context=True)
def pagination(context):
    page_num = context[b'page'].number - 1
    paginator = context[b'p']
    if not paginator.num_pages or paginator.num_pages == 1:
        page_range = []
    else:
        ON_EACH_SIDE = 3
        ON_ENDS = 2
        if paginator.num_pages <= 10:
            page_range = list(range(paginator.num_pages))
        else:
            page_range = []
            if page_num > ON_EACH_SIDE + ON_ENDS:
                page_range.extend(list(range(0, ON_EACH_SIDE - 1)))
                page_range.append(DOT)
                page_range.extend(list(range(page_num - ON_EACH_SIDE, page_num + 1)))
            else:
                page_range.extend(list(range(0, page_num + 1)))
            if page_num < paginator.num_pages - ON_EACH_SIDE - ON_ENDS - 1:
                page_range.extend(list(range(page_num + 1, page_num + ON_EACH_SIDE + 1)))
                page_range.append(DOT)
                page_range.extend(list(range(paginator.num_pages - ON_ENDS, paginator.num_pages)))
            else:
                page_range.extend(list(range(page_num + 1, paginator.num_pages)))
    return {b'page_range': page_range, 
       b'page_num': page_num, 
       b'results_var': context[b'results_var'], 
       b'query': context[b'query']}