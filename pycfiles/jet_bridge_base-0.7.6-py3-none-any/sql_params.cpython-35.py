# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/f1nal/Dropbox/python/jet-bridge/src/packages/jet_bridge_base/jet_bridge_base/fields/sql_params.py
# Compiled at: 2019-10-30 05:24:12
# Size of source mod 2**32: 509 bytes
from jet_bridge_base import fields

class SqlParamsSerializers(fields.CharField):

    def to_internal_value_item(self, value):
        value = super(SqlParamsSerializers, self).to_internal_value_item(value)
        if value is None:
            return []
        value = value.split(',')
        return dict([['param_{}'.format(i), x] for i, x in enumerate(value)])

    def to_representation_item(self, value):
        return list(value)