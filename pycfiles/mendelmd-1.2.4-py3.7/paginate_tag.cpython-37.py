# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/individuals/templatetags/paginate_tag.py
# Compiled at: 2019-05-07 08:43:55
# Size of source mod 2**32: 1114 bytes
from django import template
register = template.Library()

@register.filter
def paginator(context, adjacent_pages=2):
    """
    To be used in conjunction with the object_list generic view.

    Adds pagination context variables for use in displaying first, adjacent and
    last page links in addition to those created by the object_list generic
    view.

    """
    page_numbers = [n for n in range(context['page'] - adjacent_pages, context['page'] + adjacent_pages + 1) if n > 0 if n <= context['pages']]
    return {'hits':context['hits'], 
     'results_per_page':context['results_per_page'], 
     'page':context['page'], 
     'pages':context['pages'], 
     'page_numbers':page_numbers, 
     'next':context['next'], 
     'previous':context['previous'], 
     'has_next':context['has_next'], 
     'has_previous':context['has_previous'], 
     'show_first':1 not in page_numbers, 
     'show_last':context['pages'] not in page_numbers}