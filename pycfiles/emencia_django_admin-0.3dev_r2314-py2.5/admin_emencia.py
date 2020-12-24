# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/emencia_django_admin/templatetags/admin_emencia.py
# Compiled at: 2008-10-06 11:14:34
from django.template import Library
from django.contrib.admin.templatetags.admin_list import items_for_result, result_headers
register = Library()

def results(cl):
    for res in cl.result_list:
        yield {'id': res.id, 'items': list(items_for_result(cl, res))}


@register.inclusion_tag('admin/change_list_results.html')
def emencia_result_list(cl):
    return {'cl': cl, 'result_headers': list(result_headers(cl)), 
       'type': cl.model.__name__.lower(), 
       'results': list(results(cl))}