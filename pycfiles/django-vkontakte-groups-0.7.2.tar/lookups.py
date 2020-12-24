# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ramusus/workspace/manufacture/env/src/django-vkontakte-groups/vkontakte_groups/lookups.py
# Compiled at: 2015-02-02 04:37:57
from ajax_select import LookupChannel
from .models import Group

class VkontakteLookupChannel(LookupChannel):

    def get_pk(self, obj):
        return getattr(obj, 'remote_id')

    def get_objects(self, ids):
        ids = [ int(id) for id in ids ]
        return self.model.objects.filter(remote_id__in=ids)


class GroupLookup(VkontakteLookupChannel):
    model = Group

    def get_query(self, q, request):
        return self.model.remote.search(q=q)

    def format_item_display(self, obj):
        return unicode('<a href="%s" target="_blank">%s</a>' % (obj.get_url(), obj.name))