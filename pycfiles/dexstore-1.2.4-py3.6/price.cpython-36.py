# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dexstore/price.py
# Compiled at: 2019-03-20 14:33:32
# Size of source mod 2**32: 12859 bytes
from fractions import Fraction
from .account import Account
from .amount import Amount
from .asset import Asset
from .exceptions import InvalidAssetException
from .instance import BlockchainInstance
from .utils import assets_from_string, formatTimeString, parse_time
from graphenecommon.price import Price as GraphenePrice

@BlockchainInstance.inject
class Price(GraphenePrice):
    __doc__ = ' This class deals with all sorts of prices of any pair of assets to\n        simplify dealing with the tuple::\n\n            (quote, base)\n\n        each being an instance of :class:`dexstore.amount.Amount`. The\n        amount themselves define the price.\n\n        .. note::\n\n            The price (floating) is derived as ``base/quote``\n\n        :param list args: Allows to deal with different representations of a price\n        :param dexstore.asset.Asset base: Base asset\n        :param dexstore.asset.Asset quote: Quote asset\n        :param dexstore.dexstore.DexStore blockchain_instance: DexStore instance\n        :returns: All data required to represent a price\n        :rtype: dict\n\n        Way to obtain a proper instance:\n\n            * ``args`` is a str with a price and two assets\n            * ``args`` can be a floating number and ``base`` and ``quote`` being instances of :class:`dexstore.asset.Asset`\n            * ``args`` can be a floating number and ``base`` and ``quote`` being instances of ``str``\n            * ``args`` can be dict with keys ``price``, ``base``, and ``quote`` (*graphene balances*)\n            * ``args`` can be dict with keys ``base`` and ``quote``\n            * ``args`` can be dict with key ``receives`` (filled orders)\n            * ``args`` being a list of ``[quote, base]`` both being instances of :class:`dexstore.amount.Amount`\n            * ``args`` being a list of ``[quote, base]`` both being instances of ``str`` (``amount symbol``)\n            * ``base`` and ``quote`` being instances of :class:`dexstore.asset.Amount`\n\n        This allows instanciations like:\n\n        * ``Price("0.315 USD/DST")``\n        * ``Price(0.315, base="USD", quote="DST")``\n        * ``Price(0.315, base=Asset("USD"), quote=Asset("DST"))``\n        * ``Price({"base": {"amount": 1, "asset_id": "1.3.0"}, "quote": {"amount": 10, "asset_id": "1.3.106"}})``\n        * ``Price({"receives": {"amount": 1, "asset_id": "1.3.0"}, "pays": {"amount": 10, "asset_id": "1.3.106"}}, base_asset=Asset("1.3.0"))``\n        * ``Price(quote="10 GOLD", base="1 USD")``\n        * ``Price("10 GOLD", "1 USD")``\n        * ``Price(Amount("10 GOLD"), Amount("1 USD"))``\n        * ``Price(1.0, "USD/GOLD")``\n\n        Instances of this class can be used in regular mathematical expressions\n        (``+-*/%``) such as:\n\n        .. code-block:: python\n\n            >>> from dexstore.price import Price\n            >>> Price("0.3314 USD/DST") * 2\n            0.662600000 USD/DST\n\n    '

    def define_classes(self):
        self.amount_class = Amount
        self.asset_class = Asset

    @property
    def market(self):
        """ Open the corresponding market

            :returns: Instance of :class:`dexstore.market.Market` for the
                      corresponding pair of assets.
        """
        from .market import Market
        return Market(base=(self['base']['asset']),
          quote=(self['quote']['asset']),
          blockchain_instance=(self.blockchain))


class Order(Price):
    __doc__ = " This class inherits :class:`dexstore.price.Price` but has the ``base``\n        and ``quote`` Amounts not only be used to represent the price (as a\n        ratio of base and quote) but instead has those amounts represent the\n        amounts of an actual order!\n\n        :param dexstore.dexstore.DexStore blockchain_instance: DexStore instance\n\n        .. note::\n\n                If an order is marked as deleted, it will carry the\n                'deleted' key which is set to ``True`` and all other\n                data be ``None``.\n    "

    def __init__(self, *args, **kwargs):
        if len(args) == 1:
            if isinstance(args[0], str):
                order = self.blockchain.rpc.get_objects([args[0]])[0]
                if order:
                    Price.__init__(self, order['sell_price'])
                    self.update(order)
                    self['deleted'] = False
                else:
                    self['id'] = args[0]
                    self['deleted'] = True
                    self['quote'] = None
                    self['base'] = None
                    self['price'] = None
                    self['seller'] = None
        else:
            if isinstance(args[0], dict) and 'sell_price' in args[0]:
                self.update(args[0])
                Price.__init__(self,
                  (args[0]['sell_price']), blockchain_instance=(self.blockchain))
            else:
                if isinstance(args[0], dict) and 'min_to_receive' in args[0] and 'amount_to_sell' in args[0]:
                    self.update(args[0])
                    Price.__init__(self, Amount((args[0]['min_to_receive']), blockchain_instance=(self.blockchain)), Amount((args[0]['amount_to_sell']), blockchain_instance=(self.blockchain)))
                else:
                    (Price.__init__)(self, *args, **kwargs)
            if 'for_sale' in self:
                self['for_sale'] = Amount({'amount':self['for_sale'], 
                 'asset_id':self['base']['asset']['id']},
                  blockchain_instance=(self.blockchain))

    def __repr__(self):
        if 'deleted' in self:
            if self['deleted']:
                return 'deleted order %s' % self['id']
            else:
                t = ''
                if 'time' in self:
                    if self['time']:
                        t += '(%s) ' % self['time']
                if 'type' in self:
                    if self['type']:
                        t += '%s ' % str(self['type'])
            if 'for_sale' in self and self['for_sale']:
                t += '{} for {} '.format(str(Amount((float(self['for_sale']) / self['price']),
                  (self['quote']['asset']),
                  blockchain_instance=(self.blockchain))), str(self['for_sale']))
        else:
            if 'amount_to_sell' in self:
                t += '{} for {} '.format(str(Amount((self['amount_to_sell']),
                  blockchain_instance=(self.blockchain))), str(Amount((self['min_to_receive']),
                  blockchain_instance=(self.blockchain))))
            elif 'quote' in self:
                if 'base' in self:
                    t += '{} for {} '.format(str(Amount({'amount':self['quote'], 
                     'asset_id':self['quote']['asset']['id']},
                      blockchain_instance=(self.blockchain))), str(Amount({'amount':self['base'], 
                     'asset_id':self['base']['asset']['id']},
                      blockchain_instance=(self.blockchain))))
        return t + '@ ' + Price.__repr__(self)

    __str__ = __repr__


class FilledOrder(Price):
    __doc__ = ' This class inherits :class:`dexstore.price.Price` but has the ``base``\n        and ``quote`` Amounts not only be used to represent the price (as a\n        ratio of base and quote) but instead has those amounts represent the\n        amounts of an actually filled order!\n\n        :param dexstore.dexstore.DexStore blockchain_instance: DexStore instance\n\n        .. note:: Instances of this class come with an additional ``time`` key\n                  that shows when the order has been filled!\n    '

    def __init__(self, order, **kwargs):
        if isinstance(order, dict):
            if 'price' in order:
                Price.__init__(self,
                  (order.get('price')),
                  base=(kwargs.get('base')),
                  quote=(kwargs.get('quote')))
                self.update(order)
                self['time'] = formatTimeString(order['date'])
        else:
            if isinstance(order, dict):
                if 'op' in order:
                    order = order['op'][1]
                base_asset = kwargs.get('base_asset', order['receives']['asset_id'])
                Price.__init__(self, order, base_asset=base_asset)
                self.update(order)
                if 'time' in order:
                    self['time'] = formatTimeString(order['time'])
                if 'account_id' in order:
                    self['account_id'] = order['account_id']
            else:
                raise ValueError("Couldn't parse 'Price'.")

    def __repr__(self):
        t = ''
        if 'time' in self:
            if self['time']:
                t += '(%s) ' % self['time']
        if 'type' in self:
            if self['type']:
                t += '%s ' % str(self['type'])
        if 'quote' in self:
            if self['quote']:
                t += '%s ' % str(self['quote'])
        if 'base' in self:
            if self['base']:
                t += '%s ' % str(self['base'])
        return t + '@ ' + Price.__repr__(self)

    __str__ = __repr__


class UpdateCallOrder(Price):
    __doc__ = ' This class inherits :class:`dexstore.price.Price` but has the ``base``\n        and ``quote`` Amounts not only be used to represent the **call\n        price** (as a ratio of base and quote).\n\n        :param dexstore.dexstore.DexStore blockchain_instance: DexStore instance\n    '

    def __init__(self, call, **kwargs):
        (BlockchainInstance.__init__)(self, **kwargs)
        if isinstance(call, dict):
            if 'call_price' in call:
                Price.__init__(self,
                  (call.get('call_price')),
                  base=(call['call_price'].get('base')),
                  quote=(call['call_price'].get('quote')))
        else:
            raise ValueError("Couldn't parse 'Call'.")

    def __repr__(self):
        t = 'Margin Call: '
        if 'quote' in self:
            if self['quote']:
                t += '%s ' % str(self['quote'])
        if 'base' in self:
            if self['base']:
                t += '%s ' % str(self['base'])
        return t + '@ ' + Price.__repr__(self)

    __str__ = __repr__


@BlockchainInstance.inject
class PriceFeed(dict):
    __doc__ = ' This class is used to represent a price feed consisting of\n\n        * a witness,\n        * a symbol,\n        * a core exchange rate,\n        * the maintenance collateral ratio,\n        * the max short squeeze ratio,\n        * a settlement price, and\n        * a date\n\n        :param dexstore.dexstore.DexStore blockchain_instance: DexStore instance\n\n    '

    def __init__(self, feed, **kwargs):
        if len(feed) == 2:
            dict.__init__(self, {'producer':Account(feed[0],
               lazy=True, blockchain_instance=self.blockchain), 
             'date':parse_time(feed[1][0]), 
             'maintenance_collateral_ratio':feed[1][1]['maintenance_collateral_ratio'], 
             'maximum_short_squeeze_ratio':feed[1][1]['maximum_short_squeeze_ratio'], 
             'settlement_price':Price(feed[1][1]['settlement_price']), 
             'core_exchange_rate':Price(feed[1][1]['core_exchange_rate'])})
        else:
            dict.__init__(self, {'maintenance_collateral_ratio':feed['maintenance_collateral_ratio'], 
             'maximum_short_squeeze_ratio':feed['maximum_short_squeeze_ratio'], 
             'settlement_price':Price(feed['settlement_price']), 
             'core_exchange_rate':Price(feed['core_exchange_rate'])})