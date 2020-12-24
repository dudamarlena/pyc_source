# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /apps/xio/core/network/network.py
# Compiled at: 2018-12-07 08:05:34
# Size of source mod 2**32: 477 bytes
from xio.core.app.app import App
from xio.core.peers import Peers
from xio.core.lib.utils import is_string, urlparse
from xio.core.lib.logs import log

def network(*args, **kwargs):
    return (Network.factory)(*args, **kwargs)


class Network(App):
    peers = None

    def __init__(self, id=None, **kwargs):
        (App.__init__)(self, **kwargs)
        self.peers = Peers()
        self.network = self
        self.log = log