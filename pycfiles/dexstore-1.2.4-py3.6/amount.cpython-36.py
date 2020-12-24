# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dexstore/amount.py
# Compiled at: 2019-03-20 04:11:58
# Size of source mod 2**32: 2169 bytes
from .asset import Asset
from .instance import BlockchainInstance
from graphenecommon.amount import Amount as GrapheneAmount

@BlockchainInstance.inject
class Amount(GrapheneAmount):
    __doc__ = ' This class deals with Amounts of any asset to simplify dealing with the tuple::\n\n            (amount, asset)\n\n        :param list args: Allows to deal with different representations of an amount\n        :param float amount: Let\'s create an instance with a specific amount\n        :param str asset: Let\'s you create an instance with a specific asset (symbol)\n        :param dexstore.dexstore.DexStore blockchain_instance: DexStore instance\n        :returns: All data required to represent an Amount/Asset\n        :rtype: dict\n        :raises ValueError: if the data provided is not recognized\n\n        .. code-block:: python\n\n            from peerplays.amount import Amount\n            from peerplays.asset import Asset\n            a = Amount("1 USD")\n            b = Amount(1, "USD")\n            c = Amount("20", Asset("USD"))\n            a + b\n            a * 2\n            a += b\n            a /= 2.0\n\n        Way to obtain a proper instance:\n\n            * ``args`` can be a string, e.g.:  "1 USD"\n            * ``args`` can be a dictionary containing ``amount`` and ``asset_id``\n            * ``args`` can be a dictionary containing ``amount`` and ``asset``\n            * ``args`` can be a list of a ``float`` and ``str`` (symbol)\n            * ``args`` can be a list of a ``float`` and a :class:`dexstore.asset.Asset`\n            * ``amount`` and ``asset`` are defined manually\n\n        An instance is a dictionary and comes with the following keys:\n\n            * ``amount`` (float)\n            * ``symbol`` (str)\n            * ``asset`` (instance of :class:`dexstore.asset.Asset`)\n\n        Instances of this class can be used in regular mathematical expressions\n        (``+-*/%``) such as:\n\n        .. code-block:: python\n\n            Amount("1 USD") * 2\n            Amount("15 GOLD") + Amount("0.5 GOLD")\n    '

    def define_classes(self):
        from .price import Price
        self.asset_class = Asset
        self.price_class = Price