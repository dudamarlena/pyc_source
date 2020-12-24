# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/dpaycli/notify.py
# Compiled at: 2018-10-15 03:13:49
# Size of source mod 2**32: 2390 bytes
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import logging
from events import Events
from dpaycliapi.websocket import DPayWebsocket
from dpaycli.instance import shared_dpay_instance
from dpaycli.blockchain import Blockchain
from dpaycli.price import Order, FilledOrder
log = logging.getLogger(__name__)

class Notify(Events):
    __doc__ = ' Notifications on Blockchain events.\n\n        This modules allows yout to be notified of events taking place on the\n        blockchain.\n\n        :param fnt on_block: Callback that will be called for each block received\n        :param dpaycli.dpay.DPay dpay_instance: DPay instance\n\n        **Example**\n\n        .. code-block:: python\n\n            from pprint import pprint\n            from dpaycli.notify import Notify\n\n            notify = Notify(\n                on_block=print,\n            )\n            notify.listen()\n\n    '
    __events__ = [
     'on_block']

    def __init__(self, on_block=None, only_block_id=False, dpay_instance=None, keep_alive=25):
        Events.__init__(self)
        self.events = Events()
        self.dpay = dpay_instance or shared_dpay_instance()
        if on_block:
            self.on_block += on_block
        self.websocket = DPayWebsocket(urls=(self.dpay.rpc.nodes),
          user=(self.dpay.rpc.user),
          password=(self.dpay.rpc.password),
          only_block_id=only_block_id,
          on_block=(self.process_block),
          keep_alive=keep_alive)

    def reset_subscriptions(self, accounts=[]):
        """Change the subscriptions of a running Notify instance
        """
        self.websocket.reset_subscriptions(accounts)

    def close(self):
        """Cleanly close the Notify instance
        """
        self.websocket.close()

    def process_block(self, message):
        self.on_block(message)

    def listen(self):
        """ This call initiates the listening/notification process. It
            behaves similar to ``run_forever()``.
        """
        self.websocket.run_forever()