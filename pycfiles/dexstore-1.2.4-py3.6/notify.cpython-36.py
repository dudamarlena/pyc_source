# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dexstore/notify.py
# Compiled at: 2019-03-20 04:11:58
# Size of source mod 2**32: 5924 bytes
import logging
from dexstoreapi.websocket import DexStoreWebsocket
from events import Events
from .account import AccountUpdate
from .instance import BlockchainInstance
from .market import Market
from .price import FilledOrder, Order, UpdateCallOrder
log = logging.getLogger(__name__)

class Notify(Events, BlockchainInstance):
    __doc__ = ' Notifications on Blockchain events.\n\n        :param list accounts: Account names/ids to be notified about when changing\n        :param list markets: Instances of :class:`dexstore.market.Market` that identify markets to be monitored\n        :param list objects: Object ids to be notified about when changed\n        :param fnt on_tx: Callback that will be called for each transaction received\n        :param fnt on_block: Callback that will be called for each block received\n        :param fnt on_account: Callback that will be called for changes of the listed accounts\n        :param fnt on_market: Callback that will be called for changes of the listed markets\n        :param dexstore.dexstore.DexStore blockchain_instance: DexStore instance\n\n        **Example**\n\n        .. code-block:: python\n\n            from pprint import pprint\n            from dexstore.notify import Notify\n            from dexstore.market import Market\n\n            notify = Notify(\n                markets=["TEST:GOLD"],\n                accounts=["xeroc"],\n                on_market=print,\n                on_account=print,\n                on_block=print,\n                on_tx=print\n            )\n            notify.listen()\n\n\n    '
    __events__ = [
     'on_tx', 'on_object', 'on_block', 'on_account', 'on_market']

    def __init__(self, accounts=[], markets=[], objects=[], on_tx=None, on_object=None, on_block=None, on_account=None, on_market=None, keep_alive=25, **kwargs):
        super(Notify, self).__init__()
        self.events = Events()
        (BlockchainInstance.__init__)(self, **kwargs)
        if on_tx:
            self.on_tx += on_tx
        if on_object:
            self.on_object += on_object
        if on_block:
            self.on_block += on_block
        if on_account:
            self.on_account += on_account
        if on_market:
            self.on_market += on_market
        self.websocket = DexStoreWebsocket(urls=(self.blockchain.rpc.urls),
          user=(self.blockchain.rpc.user),
          password=(self.blockchain.rpc.password),
          accounts=accounts,
          markets=(self.get_market_ids(markets)),
          objects=objects,
          on_tx=on_tx,
          on_object=on_object,
          on_block=on_block,
          on_account=(self.process_account),
          on_market=(self.process_market),
          keep_alive=keep_alive)

    def get_market_ids(self, markets):
        market_ids = []
        for market_name in markets:
            market = Market(market_name, blockchain_instance=(self.blockchain))
            market_ids.append([market['base']['id'], market['quote']['id']])

        return market_ids

    def reset_subscriptions(self, accounts=[], markets=[], objects=[]):
        """Change the subscriptions of a running Notify instance
        """
        self.websocket.reset_subscriptions(accounts, self.get_market_ids(markets), objects)

    def close(self):
        """Cleanly close the Notify instance
        """
        self.websocket.close()

    def process_market(self, data):
        """ This method is used for post processing of market
            notifications. It will return instances of either

            * :class:`dexstore.price.Order` or
            * :class:`dexstore.price.FilledOrder` or
            * :class:`dexstore.price.UpdateCallOrder`

            Also possible are limit order updates (margin calls)

        """
        for d in data:
            if not d:
                pass
            else:
                if isinstance(d, str):
                    log.debug('Calling on_market with Order()')
                    self.on_market(Order(d, blockchain_instance=(self.blockchain)))
                    continue
                else:
                    if isinstance(d, dict):
                        d = [
                         d]
                for p in d:
                    if not isinstance(p, list):
                        p = [
                         p]
                    for i in p:
                        if isinstance(i, dict):
                            if 'pays' in i and 'receives' in i:
                                self.on_market(FilledOrder(i, blockchain_instance=(self.blockchain)))
                        if 'for_sale' in i and 'sell_price' in i:
                            self.on_market(Order(i, blockchain_instance=(self.blockchain)))
                        elif 'collateral' in i and 'call_price' in i:
                            self.on_market(UpdateCallOrder(i, blockchain_instance=(self.blockchain)))
                        else:
                            if i:
                                log.error('Unknown market update type: %s' % i)

    def process_account(self, message):
        """ This is used for processing of account Updates. It will
            return instances of :class:dexstore.account.AccountUpdate`
        """
        self.on_account(AccountUpdate(message, blockchain_instance=(self.blockchain)))

    def listen(self):
        """ This call initiates the listening/notification process. It
            behaves similar to ``run_forever()``.
        """
        self.websocket.run_forever()