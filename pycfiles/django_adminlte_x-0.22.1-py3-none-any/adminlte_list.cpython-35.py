# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\django\hris\adminlte\templatetags\adminlte_list.py
# Compiled at: 2017-05-04 04:05:10
# Size of source mod 2**32: 236 bytes
from django.contrib.admin.templatetags.admin_list import pagination
from django.template import Library
register = Library()

@register.inclusion_tag('admin/pagination_top.html')
def pagination_top(cl):
    return pagination(cl)