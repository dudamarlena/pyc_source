# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/emencia_django_admin/templatetags/admin_csv.py
# Compiled at: 2008-10-06 11:14:34
from django.template import Library
register = Library()

@register.inclusion_tag('admin/filter_select.html')
def admin_list_filter_selector(cl, spec):
    choices = []
    for choice in spec.choices(cl):
        query = choice['query_string']
        query = query[1:]
        choice['query_string'] = query
        choices.append(choice)

    return {'title': spec.title(), 'choices': choices}