# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vsm/api/views/types.py
# Compiled at: 2016-06-13 14:11:03
from vsm.api import common

class ViewBuilder(common.ViewBuilder):

    def show(self, request, storage_type, brief=False):
        """Trim away extraneous storage type attributes."""
        trimmed = dict(id=storage_type.get('id'), name=storage_type.get('name'), extra_specs=storage_type.get('extra_specs'))
        if brief:
            return trimmed
        return dict(storage_type=trimmed)

    def index(self, request, storage_types):
        """Index over trimmed storage types"""
        storage_types_list = [ self.show(request, storage_type, True) for storage_type in storage_types ]
        return dict(storage_types=storage_types_list)