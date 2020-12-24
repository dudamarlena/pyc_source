# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djblets/datagrid/templatetags/datagrid.py
# Compiled at: 2019-06-12 01:17:17
from __future__ import unicode_literals
import warnings
from django import template
from djblets.deprecation import RemovedInDjblets20Warning
register = template.Library()

@register.inclusion_tag(b'datagrid/paginator.html', takes_context=True)
def paginator(context, adjacent_pages=3):
    """Renders a paginator used for jumping between pages of results."""
    warnings.warn(b'djblets.datagrid.templatetags datagrid is deprecated, Use DataGrid.render_paginator', RemovedInDjblets20Warning)
    page_nums = range(max(1, context[b'page'] - adjacent_pages), min(context[b'pages'], context[b'page'] + adjacent_pages) + 1)
    extra_query = context.get(b'extra_query', None)
    if extra_query:
        extra_query += b'&'
    return {b'hits': context[b'hits'], 
       b'results_per_page': context[b'results_per_page'], 
       b'page': context[b'page'], 
       b'pages': context[b'pages'], 
       b'page_numbers': page_nums, 
       b'next': context[b'next'], 
       b'previous': context[b'previous'], 
       b'has_next': context[b'has_next'], 
       b'has_previous': context[b'has_previous'], 
       b'show_first': 1 not in page_nums, 
       b'show_last': context[b'pages'] not in page_nums, 
       b'extra_query': extra_query}