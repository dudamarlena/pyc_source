# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/electrum_chi/electrum/plugins/safe_t/client.py
# Compiled at: 2019-08-24 06:06:43
# Size of source mod 2**32: 437 bytes
from safetlib.client import proto, BaseClient, ProtocolMixin
from .clientbase import SafeTClientBase

class SafeTClient(SafeTClientBase, ProtocolMixin, BaseClient):

    def __init__(self, transport, handler, plugin):
        BaseClient.__init__(self, transport=transport)
        ProtocolMixin.__init__(self, transport=transport)
        SafeTClientBase.__init__(self, handler, plugin, proto)


SafeTClientBase.wrap_methods(SafeTClient)