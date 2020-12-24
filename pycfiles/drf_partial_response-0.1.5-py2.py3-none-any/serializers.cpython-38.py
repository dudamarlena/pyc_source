# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/thongnguyen/training/asoft/thongnguyen/python-tools/drf-partial-response/drf_partial_response/serializers.py
# Compiled at: 2020-03-20 04:14:40
# Size of source mod 2**32: 1424 bytes
from __future__ import unicode_literals
from django.utils.functional import cached_property
from jsonmask import should_include_variable
from .utils import collapse_includes_excludes

class FieldsListSerializerMixin(object):

    @cached_property
    def _readable_fields(self):
        readable_fields = super(FieldsListSerializerMixin, self)._readable_fields
        return self.prune_readable_fields(readable_fields)

    def prune_readable_fields(self, readable_fields):
        requested_fields = self._context.get('requested_fields') or {}
        excluded_fields = self._context.get('excluded_fields') or {}
        structure, is_negated = collapse_includes_excludes(requested_fields, excluded_fields)
        pruned_fields = [field for field in readable_fields if should_include_variable((field.field_name),
          structure, is_negated=is_negated)]
        for field in pruned_fields:
            field._context = self._context.copy()
            field._context['requested_fields'] = requested_fields.copy().get(field.field_name)
            field._context['excluded_fields'] = excluded_fields.copy().get(field.field_name)
            if hasattr(field, 'child'):
                field.child._context = field._context.copy()
            return pruned_fields