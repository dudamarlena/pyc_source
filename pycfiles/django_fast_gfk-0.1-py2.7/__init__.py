# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fast_gfk/__init__.py
# Compiled at: 2017-07-19 04:09:54
"""We use the word "target" to denote the value of the generic foreign key."""

class Wrapper(object):

    def __init__(self, context, target, target_field='target'):
        self._context = context
        self._target = target
        self._target_field = target_field

    def __getattr__(self, name):
        if name == self._target_field:
            return self._target
        try:
            return super(Wrapper, self).__getattr__(name)
        except AttributeError:
            return getattr(self._context, name)


def fetch(queryset, field='content_object'):
    from django.contrib.contenttypes.models import ContentType
    map_ct_targets = {}
    map_two_deep = {}
    for obj in queryset:
        gfk_field = obj._meta.get_field(field)
        ct_id = getattr(obj, gfk_field.ct_field + '_id')
        obj_id = getattr(obj, gfk_field.fk_field)
        if ct_id not in map_ct_targets:
            map_ct_targets[ct_id] = []
        map_ct_targets[ct_id].append(obj_id)
        if ct_id not in map_two_deep:
            map_two_deep[ct_id] = {}
        if obj_id not in map_two_deep[ct_id]:
            map_two_deep[ct_id][obj_id] = []
        map_two_deep[ct_id][obj_id].append(obj)

    content_types = {}
    for ct in ContentType.objects.filter(id__in=map_ct_targets.keys()):
        content_types[ct.id] = ct

    wrapped_objects = {}
    for ct_id, ids in map_ct_targets.items():
        for obj in content_types[ct_id].model_class().objects.filter(id__in=ids):
            for item in map_two_deep[ct_id][obj.id]:
                wrapped_objects[item.id] = Wrapper(item, target=obj)

    for obj in queryset:
        yield wrapped_objects[obj.id]