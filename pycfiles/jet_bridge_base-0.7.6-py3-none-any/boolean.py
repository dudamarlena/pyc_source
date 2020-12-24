# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/f1nal/Dropbox/python/jet-bridge/src/packages/jet_bridge_base/jet_bridge_base/fields/boolean.py
# Compiled at: 2019-09-29 04:07:46
from jet_bridge_base.fields.field import Field

class BooleanField(Field):
    TRUE_VALUES = {
     't', 'T',
     'y', 'Y', 'yes', 'YES',
     'true', 'True', 'TRUE',
     'on', 'On', 'ON',
     '1', 1,
     True}
    FALSE_VALUES = {
     'f', 'F',
     'n', 'N', 'no', 'NO',
     'false', 'False', 'FALSE',
     'off', 'Off', 'OFF',
     '0', 0, 0.0,
     False}

    def to_internal_value_item(self, value):
        if value in self.TRUE_VALUES:
            return True
        if value in self.FALSE_VALUES:
            return False
        return bool(value)

    def to_representation_item(self, value):
        return value