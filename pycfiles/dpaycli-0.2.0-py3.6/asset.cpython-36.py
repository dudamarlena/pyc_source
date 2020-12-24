# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/dpaycli/asset.py
# Compiled at: 2018-10-15 03:20:54
# Size of source mod 2**32: 2852 bytes
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import json
from .exceptions import AssetDoesNotExistsException
from .blockchainobject import BlockchainObject

class Asset(BlockchainObject):
    __doc__ = ' Deals with Assets of the network.\n\n        :param str Asset: Symbol name or object id of an asset\n        :param bool lazy: Lazy loading\n        :param bool full: Also obtain bitasset-data and dynamic asset dat\n        :param dpaycli.dpay.DPay dpay_instance: DPay\n            instance\n        :returns: All data of an asset\n\n        .. note:: This class comes with its own caching function to reduce the\n                  load on the API server. Instances of this class can be\n                  refreshed with ``Asset.refresh()``.\n    '
    type_id = 3

    def __init__(self, asset, lazy=False, full=False, dpay_instance=None):
        self.full = full
        super(Asset, self).__init__(asset,
          lazy=lazy,
          full=full,
          dpay_instance=dpay_instance)

    def refresh(self):
        """ Refresh the data from the API server
        """
        self.chain_params = self.dpay.get_network()
        if self.chain_params is None:
            from dpaycligraphenebase.chains import known_chains
            self.chain_params = known_chains['DPAY']
        self['asset'] = ''
        found_asset = False
        for asset in self.chain_params['chain_assets']:
            if self.identifier in [asset['symbol'], asset['asset'], asset['id']]:
                self['asset'] = asset['asset']
                self['precision'] = asset['precision']
                self['id'] = asset['id']
                self['symbol'] = asset['symbol']
                found_asset = True
                break

        if not found_asset:
            raise AssetDoesNotExistsException(self.identifier + ' chain_assets:' + str(self.chain_params['chain_assets']))

    @property
    def symbol(self):
        return self['symbol']

    @property
    def asset(self):
        return self['asset']

    @property
    def precision(self):
        return self['precision']

    def __eq__(self, other):
        if isinstance(other, (Asset, dict)):
            return self['symbol'] == other['symbol'] and self['asset'] == other['asset'] and self['precision'] == other['precision']
        else:
            return self['symbol'] == other

    def __ne__(self, other):
        if isinstance(other, (Asset, dict)):
            return self['symbol'] != other['symbol'] or self['asset'] != other['asset'] or self['precision'] != other['precision']
        else:
            return self['symbol'] != other