# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/f1nal/Dropbox/python/jet-bridge/src/packages/jet_bridge_base/jet_bridge_base/fields/array.py
# Compiled at: 2019-09-29 04:07:46
import json
from jet_bridge_base.fields.field import Field

class ArrayField(Field):

    def to_internal_value_item(self, value):
        return json.loads(value)

    def to_representation_item(self, value):
        return json.dumps(value)