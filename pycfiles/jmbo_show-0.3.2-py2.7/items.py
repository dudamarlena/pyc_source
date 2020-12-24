# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hedley/django/instances/foundry/src/jmbo-show/show/view_modifiers/items.py
# Compiled at: 2013-09-27 03:40:37
from jmbo.models import ModelBase
from jmbo.view_modifiers.items import GetItem

class CategoryRelatedItem(GetItem):

    def modify(self, view):
        category = self.request.GET.get(self.get['name'], 'all')
        obj = ModelBase.permitted.get(slug=view.params['slug'])
        qs = obj.get_permitted_related_items(direction='both')
        if category != 'all':
            qs = qs.filter(primary_category__slug=category)
        view.params['extra_context']['view_modifier'].related_items = qs
        view.params['extra_context']['view_modifier'].category = category
        return view