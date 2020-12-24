# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/electrum_chi/electrum/compatibility_rpc.py
# Compiled at: 2019-08-24 06:36:07
# Size of source mod 2**32: 4194 bytes
"""
A JSON-RPC server that implements methods required by games in exactly the
same way as Xaya Core does, executing them based on Electrum.  This server
can be run in addition to the "standard" Electrum JSON-RPC server, and
allows to connect games to Electrum that are originally written for the
Xaya Core JSON-RPC interface.
"""
from . import bitcoin
from . import crypto
from . import ecc
from .jsonrpc import VerifyingJSONRPCServer
from . import util
import base64

class Server(VerifyingJSONRPCServer):
    __doc__ = '\n  The compatibility JSON-RPC server instance.\n  '

    def __init__(self, *args, cmd_runner, **kwargs):
        self.cmd_runner = cmd_runner
        (VerifyingJSONRPCServer.__init__)(self, *args, **kwargs)
        self.register_function(self.getbalance, 'getbalance')
        self.register_function(self.getnewaddress, 'getnewaddress')
        self.register_function(self.signmessage, 'signmessage')
        self.register_function(self.verifymessage, 'verifymessage')
        self.register_function(self.name_list, 'name_list')
        self.register_function(self.name_pending, 'name_pending')
        self.register_function(self.name_register, 'name_register')
        self.register_function(self.name_update, 'name_update')

    def getbalance(self):
        bal = self.cmd_runner.getbalance()
        return bal['confirmed']

    def getnewaddress(self, label='', address_type=None):
        addr = self.cmd_runner.createnewaddress()
        if address_type is None:
            return addr
        if address_type == 'legacy':
            if addr.startswith('chi') or addr[0] not in ('C', 'c'):
                raise RuntimeError('Cannot produce legacy address from this wallet')
            return addr
        raise RuntimeError(f"Unsupported address type: {address_type}")

    def signmessage(self, address, message):
        return self.cmd_runner.signmessage(address, message)

    def verifymessage(self, address, signature, message):
        if address == '':
            sig = base64.b64decode(signature)
            msg_hash = crypto.sha256d(ecc.msg_magic(util.to_bytes(message)))
            pubkey, comp = ecc.ECPubkey.from_signature65(sig, msg_hash)
            address = bitcoin.public_key_to_p2pkh(pubkey.get_public_key_bytes(comp))
            addr_recovery = True
        else:
            addr_recovery = False
        res = self.cmd_runner.verifymessage(address, signature, message)
        if not addr_recovery:
            return res
        return {'valid':res,  'address':address}

    def name_list(self, name=None):
        return self.cmd_runner.name_list(name)

    def name_pending(self, name=None):
        self.logger.warning('name_pending is not supported properly, returning empty mempool')
        return []

    def name_register(self, name, value):
        tx = self.cmd_runner.name_register(name, value)
        return self.cmd_runner.broadcast(tx['hex'])

    def name_update(self, name, value):
        tx = self.cmd_runner.name_update(name, value)
        return self.cmd_runner.broadcast(tx['hex'])