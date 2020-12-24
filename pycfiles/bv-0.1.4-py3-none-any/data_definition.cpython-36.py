# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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