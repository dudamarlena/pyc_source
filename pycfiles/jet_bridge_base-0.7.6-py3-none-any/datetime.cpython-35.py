# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/f1nal/Dropbox/python/jet-bridge/src/packages/jet_bridge_base/jet_bridge_base/fields/datetime.py
# Compiled at: 2019-10-30 05:24:12
# Size of source mod 2**32: 642 bytes
import dateparser, six
from jet_bridge_base.fields.field import Field

class DateTimeField(Field):
    field_error_messages = {'invalid': 'date has wrong format'}

    def to_internal_value_item(self, value):
        if value is None:
            return
        value = six.text_type(value).strip()
        try:
            result = dateparser.parse(value)
        except ValueError:
            result = None

        if result is None:
            self.error('invalid')
        return result

    def to_representation_item(self, value):
        if value is None:
            return
        return value.isoformat()