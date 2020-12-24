# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/libcontractvm/Wallet.py
# Compiled at: 2015-11-05 10:05:28
# Size of source mod 2**32: 3672 bytes
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
import logging, json, requests, binascii
from . import Log
logger = logging.getLogger('libcontractvm')

class Wallet:

    def __init__(self, chain='XTN', address=None, wif=None, wallet_file=None):
        self.address = address
        self.wif = wif
        self.wallet_file = wallet_file
        self.chain = chain
        if self.address == None or self.wif == None:
            if self.wallet_file != None:
                try:
                    f = open(self.wallet_file, 'r')
                    d = f.read()
                    f.close()
                    d = d.split(',')
                    self.address = d[0]
                    self.wif = d[1].replace('\n', '')
                    logger.info('Loaded wallet from %s', self.wallet_file)
                except:
                    self.address = None
                    self.wif = None
                    logger.info('Failed to load wallet from %s', self.wallet_file)

            if self.wif == None:
                logger.info('Generating new key pair')
                self.address, self.wif = self._gen()
                if self.wallet_file != None:
                    f = open(self.wallet_file, 'w')
                    f.write(self.address + ',' + self.wif)
                    f.close()
                    logger.info('Saved wallet to %s', self.wallet_file)
        elif self.wallet_file != None:
            f = open(self.wallet_file, 'w')
            f.write(self.address + ',' + self.wif)
            f.close()
        logger.info('Setting up player %s', self.address)

    def _gen(self):
        logger.debug('Generating entropy for new wallet...')
        entropy = bytearray()
        try:
            entropy.extend(open('/dev/random', 'rb').read(64))
        except Exception:
            print("warning: can't use /dev/random as entropy source")

        entropy = bytes(entropy)
        if len(entropy) < 64:
            raise OSError("can't find sources of entropy")
        secret_exponent = int(binascii.hexlify(entropy)[0:32], 16)
        wif = secret_exponent_to_wif(secret_exponent, compressed=True, wif_prefix=wif_prefix_for_netcode(self.chain))
        key = Key(secret_exponent=secret_exponent, netcode=self.chain)
        return (str(key.address()), str(key.wif()))

    def createTransaction(self, outs, fee):
        spendables = self._spendables(int(fee))
        if len(spendables) == 0:
            logger.error('No spendables available')
            return
        t = create_tx(spendables, [self.address], fee=int(fee))
        for o in outs:
            t.txs_out.append(TxOut(0.0, tools.compile(o)))

        secret_exponent = wif_to_secret_exponent(self.wif, allowable_wif_prefixes=[wif_prefix_for_netcode(self.chain)])
        d = {}
        d.update(build_hash160_lookup([secret_exponent]))
        t.sign(d)
        txhash = t.as_hex()
        return txhash

    def getAddress(self):
        return self.address

    def getBalance(self):
        pass

    def getPair(self):
        return (
         self.address, self.wif)