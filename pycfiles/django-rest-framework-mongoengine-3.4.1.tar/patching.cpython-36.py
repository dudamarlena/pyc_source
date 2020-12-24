# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: w:\projects\django-rest-framework-mongoengine\rest_framework_mongoengine\contrib\patching.py
# Compiled at: 2019-09-19 16:31:31
# Size of source mod 2**32: 3922 bytes
import re
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.serializers import DictField, ListSerializer

def get_field_for_path(serializer, path):
    head = path[0]
    tail = path[1:]
    if hasattr(serializer, 'fields'):
        serializer = serializer.fields[head]
    else:
        if hasattr(serializer, 'child'):
            serializer = serializer.child
        else:
            raise KeyError(head)
    if len(tail):
        return get_field_for_path(serializer, tail)
    else:
        return serializer


class PatchItem(DictField):
    __doc__ = ' just a dict with keys: path, op, value '

    def to_internal_value(self, value):
        value = super(PatchItem, self).to_internal_value(value)
        if set(value.keys()) != set(['op', 'path', 'value']):
            raise ValidationError("Missing some of required parts: 'path', 'op', 'value'")
        if value['path'][0] != '/':
            raise ValidationError({'path': 'Invalid path'})
        value['path'] = tuple(value['path'].split('/')[1:])
        if self.parent.serializer:
            try:
                field = get_field_for_path(self.parent.serializer, value['path'])
            except KeyError as e:
                raise ValidationError({'path': "Missing elem: '%s'" % e.args[0]})

            if value['op'] in ('set', 'inc', 'dec'):
                if field is not None:
                    value['value'] = field.to_internal_value(value['value'])
            else:
                if value['op'] in ('push', 'pull', 'add_to_set'):
                    field = getattr(field, 'child')
                    if field is not None:
                        value['value'] = field.to_internal_value(value['value'])
                else:
                    if value['op'] in ('unset', 'pull_all', 'min', 'max'):
                        if value['value'] is not None:
                            raise ValidationError({'value': "Value for '%s' expected to be null" % value['op']})
                    elif value['op'] in ('pop', ):
                        try:
                            value['value'] = int(value['value'])
                        except:
                            raise ValidationError({'value': "Integer expected for '%s'" % value['op']})

        return value


idx_re = re.compile('^(\\d+|S)$')

class Patch(ListSerializer):
    __doc__ = ' RFC 6902 json-patch\n\n    patch := [ item ]\n    item := {\n        path: str -- path to attribute, starting with "/"\n        op: str -- mongo update operator\n        value: any -- argument to operator\n    }\n    '
    child = PatchItem()

    def __init__(self, serializer=None, *args, **kwargs):
        self.serializer = serializer if serializer is not None else None
        (super(Patch, self).__init__)(*args, **kwargs)

    def update_queryset(self, queryset):
        for item in self.validated_data:
            update = {item['op'] + '__' + '__'.join(item['path']): item['value']}
            (queryset.update)(**update)


class PatchModelMixin:
    __doc__ = '\n    Patch model instance, or requested filtered queryset.\n\n    Route PATCH request method to `modify_obj` or `modify_set`. Override `perform_modify` if necessary.\n\n    Default methods return 204 no content.\n    '

    def modify_set(self, request, *args, **kwargs):
        return self.modify_queryset(request, self.filter_queryset(self.get_queryset()))

    def modify_obj(self, request, *args, **kwargs):
        return self.modify_queryset(request, self.get_object())

    def modify_queryset(self, request, queryset):
        patch = Patch((self.get_serializer()), data=(request.data))
        patch.is_valid(raise_exception=True)
        self.perform_modify(queryset, patch)
        return Response(status=(status.HTTP_204_NO_CONTENT))

    def perform_modify(self, queryset, patch):
        """ actually perform update on queryset """
        patch.update_queryset(queryset)