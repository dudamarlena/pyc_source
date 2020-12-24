# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/f1nal/Dropbox/python/jet-bridge/src/packages/jet_bridge_base/jet_bridge_base/fields/wkt.py
# Compiled at: 2019-11-08 11:55:37
# Size of source mod 2**32: 643 bytes
import six
from jet_bridge_base.fields.field import Field

class WKTField(Field):
    field_error_messages = {'invalid': 'not a valid Geo object - {error}'}

    def to_internal_value_item(self, value):
        if value is None:
            return
        from geoalchemy2 import ArgumentError, WKTElement
        try:
            return WKTElement(value)
        except ArgumentError as e:
            self.error('invalid', error=six.text_type(e))

    def to_representation_item(self, value):
        if value is None:
            return
        from geoalchemy2.shape import to_shape
        return to_shape(value).to_wkt()