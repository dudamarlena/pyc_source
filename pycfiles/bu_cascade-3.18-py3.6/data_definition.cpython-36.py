# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/bu_cascade/assets/data_definition.py
# Compiled at: 2019-10-30 15:19:36
# Size of source mod 2**32: 438 bytes
__author__ = 'ces55739'
from bu_cascade.assets.asset import Asset

class DataDefinition(Asset):

    def __init__(self, ws_connector, identifier=None, asset=None):
        super(self.__class__, self).__init__(ws_connector, identifier, asset_type='datadefinition', asset_specific_key='dataDefinition')
        if identifier is not None:
            self.read_asset()
        elif asset is not None:
            self.create_asset(asset)