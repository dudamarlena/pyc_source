# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/julio.rama/git/vault-opensource/vault/templatetags/pagination.py
# Compiled at: 2020-03-17 15:36:47
# Size of source mod 2**32: 304 bytes
from django import template
register = template.Library()

@register.inclusion_tag('vault/pagination.html', takes_context=True)
def pagination(context, paginated_item):
    return {'items':paginated_item, 
     'get_parameters':context['request'].GET.dict()}