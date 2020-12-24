# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/f1nal/Dropbox/python/jet-bridge/src/packages/jet_bridge_base/jet_bridge_base/fields/array.py
# Compiled at: 2019-11-10 03:13:18
# Size of source mod 2**32: 542 bytes
from __future__ import absolute_import
import json
from jet_bridge_base.fields.field import Field

class ArrayField(Field):
    field_error_messages = {'invalid': 'not a valid array'}

    def to_internal_value_item(self, value):
        try:
            result = json.loads(value)
            if not isinstance(result, list):
                raise ValueError
            return result
        except ValueError:
            self.error('invalid')

    def to_representation_item(self, value):
        return json.dumps(value)