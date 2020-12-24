# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/f1nal/Dropbox/python/jet-bridge/src/packages/jet_bridge_base/jet_bridge_base/fields/integer.py
# Compiled at: 2019-10-30 05:24:12
# Size of source mod 2**32: 545 bytes
import six
from jet_bridge_base.fields.field import Field

class IntegerField(Field):
    field_error_messages = {'invalid': 'not a valid integer'}

    def to_internal_value_item(self, value):
        if value is None:
            return
        value = six.text_type(value).strip()
        try:
            return int(value)
        except (ValueError, TypeError):
            self.error('invalid')

    def to_representation_item(self, value):
        if value is None:
            return
        else:
            return six.text_type(value)