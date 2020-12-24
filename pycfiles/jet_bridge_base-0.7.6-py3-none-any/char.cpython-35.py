# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/f1nal/Dropbox/python/jet-bridge/src/packages/jet_bridge_base/jet_bridge_base/fields/char.py
# Compiled at: 2019-10-30 05:24:12
# Size of source mod 2**32: 570 bytes
import six
from jet_bridge_base.fields.field import Field

class CharField(Field):

    def __init__(self, *args, **kwargs):
        self.trim_whitespace = kwargs.pop('trim_whitespace', True)
        super(CharField, self).__init__(*args, **kwargs)

    def to_internal_value_item(self, value):
        if value is None:
            return
        value = six.text_type(value)
        if self.trim_whitespace:
            return value.strip()
        return value

    def to_representation_item(self, value):
        if value is None:
            return
        return six.text_type(value)