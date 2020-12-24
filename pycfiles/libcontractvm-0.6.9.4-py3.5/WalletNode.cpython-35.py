# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/libcontractvm/WalletNode.py
# Compiled at: 2015-11-30 12:41:35
# Size of source mod 2**32: 2355 bytes
from pycoin.networks import *
from pycoin.key import Key
from pycoin.key.BIP32Node import BIP32Node
from pycoin import encoding
from pycoin.ecdsa import is_public_pair_valid, generator_secp256k1, public_pair_for_x, secp256k1
from pycoin.serialize import b2h, h2b
from pycoin.tx import *
from pycoin.tx.tx_utils import sign_tx, create_tx
from pycoin.tx.Spendable import Spendable
from pycoin.tx.TxOut import TxOut
from pycoin.tx.script import tools
from pycoin.encoding import bitcoin_address_to_hash160_sec, is_sec_compressed, public_pair_to_sec, secret_exponent_to_wif, public_pair_to_bitcoin_address, wif_to_tuple_of_secret_exponent_compressed, sec_to_public_pair, public_pair_to_hash160_sec, wif_to_secret_exponent
from pycoin.tx.pay_to import address_for_pay_to_script, build_hash160_lookup
import logging, json, requests, binascii, requests, random
from . import Log
from libcontractvm import Wallet
logger = logging.getLogger('libcontractvm')

class WalletNode(Wallet.Wallet):

    def __init__(self, chain='XTN', address=None, wif=None, wallet_file=None, url=None):
        self.url = url
        super(WalletNode, self).__init__(chain, address, wif, wallet_file)

    def _do_request(self, command, args=[]):
        payload = {'method': command, 
         'params': args, 
         'jsonrpc': '2.0', 
         'id': 0}
        return requests.post(self.url, data=json.dumps(payload), headers={'content-type': 'application/json'}).json()

    def _spendables(self, value):
        r = self._do_request('listunspent')['result']
        random.shuffle(r)
        sps = []
        tot = 0
        for s in r:
            if s['address'] != self.address:
                pass
            else:
                txid = ''
                for x in range(len(s['txid']), -2, -2):
                    txid += s['txid'][x:x + 2]

                tot += int(float(s['amount']) * 100000000)
                sps.append(Spendable.from_dict({'coin_value': int(float(s['amount']) * 100000000), 
                 'script_hex': s['scriptPubKey'], 'tx_hash_hex': txid, 'tx_out_index': int(s['vout'])}))
                if tot >= value:
                    return sps

        return sps

    def getBalance(self):
        r = self._do_request('getaccount', [self.address])['result']
        r = self._do_request('getbalance', [r])['result']
        return float(r)