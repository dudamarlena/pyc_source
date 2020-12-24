# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/electrum_chi/electrum/constants.py
# Compiled at: 2019-08-24 07:36:23
# Size of source mod 2**32: 4482 bytes
import os, json
from .util import inv_dict

def read_json(filename, default):
    path = os.path.join(os.path.dirname(__file__), filename)
    try:
        with open(path, 'r') as (f):
            r = json.loads(f.read())
    except:
        r = default

    return r


GIT_REPO_URL = 'https://github.com/xaya/electrum-chi'
GIT_REPO_ISSUES_URL = 'https://github.com/xaya/electrum-chi/issues'

class AbstractNet:

    @classmethod
    def max_checkpoint(cls) -> int:
        return max(0, len(cls.CHECKPOINTS) * 2016 - 1)


class BitcoinMainnet(AbstractNet):
    TESTNET = False
    WIF_PREFIX = 130
    ADDRTYPE_P2PKH = 28
    ADDRTYPE_P2SH = 30
    SEGWIT_HRP = 'chi'
    GENESIS = 'e5062d76e5f50c42f493826ac9920b63a8def2626fd70a5cec707ec47a4c4651'
    DEFAULT_PORTS = {'t':'50001',  's':'50002'}
    DEFAULT_SERVERS = read_json('servers.json', {})
    CHECKPOINTS = read_json('checkpoints.json', [])
    XPRV_HEADERS = {'standard':76066276, 
     'p2wpkh-p2sh':77428856, 
     'p2wsh-p2sh':43364357, 
     'p2wpkh':78791436, 
     'p2wsh':44726937}
    XPRV_HEADERS_INV = inv_dict(XPRV_HEADERS)
    XPUB_HEADERS = {'standard':76067358, 
     'p2wpkh-p2sh':77429938, 
     'p2wsh-p2sh':43365439, 
     'p2wpkh':78792518, 
     'p2wsh':44728019}
    XPUB_HEADERS_INV = inv_dict(XPUB_HEADERS)
    BIP44_COIN_TYPE = 7


class BitcoinTestnet(AbstractNet):
    TESTNET = True
    WIF_PREFIX = 230
    ADDRTYPE_P2PKH = 88
    ADDRTYPE_P2SH = 90
    SEGWIT_HRP = 'chitn'
    GENESIS = '5195fc01d0e23d70d1f929f21ec55f47e1c6ea1e66fae98ee44cbbc994509bba'
    DEFAULT_PORTS = {'t':'51001',  's':'51002'}
    DEFAULT_SERVERS = read_json('servers_testnet.json', {})
    CHECKPOINTS = read_json('checkpoints_testnet.json', [])
    XPRV_HEADERS = {'standard':70615956, 
     'p2wpkh-p2sh':71978536, 
     'p2wsh-p2sh':37914037, 
     'p2wpkh':73341116, 
     'p2wsh':39276616}
    XPRV_HEADERS_INV = inv_dict(XPRV_HEADERS)
    XPUB_HEADERS = {'standard':70617039, 
     'p2wpkh-p2sh':71979618, 
     'p2wsh-p2sh':37915119, 
     'p2wpkh':73342198, 
     'p2wsh':39277699}
    XPUB_HEADERS_INV = inv_dict(XPUB_HEADERS)
    BIP44_COIN_TYPE = 1


class BitcoinRegtest(BitcoinTestnet):
    SEGWIT_HRP = 'chirt'
    GENESIS = '6f750b36d22f1dc3d0a6e483af45301022646dfc3b3ba2187865f5a7d6d83ab1'
    DEFAULT_SERVERS = read_json('servers_regtest.json', {})
    CHECKPOINTS = []


class BitcoinSimnet(BitcoinTestnet):
    SEGWIT_HRP = 'sb'
    GENESIS = '683e86bd5c6d110d91b94b97137ba6bfe02dbbdb8e3dff722a669b5d69d77af6'
    DEFAULT_SERVERS = read_json('servers_regtest.json', {})
    CHECKPOINTS = []


net = BitcoinMainnet

def set_simnet():
    global net
    net = BitcoinSimnet


def set_mainnet():
    global net
    net = BitcoinMainnet


def set_testnet():
    global net
    net = BitcoinTestnet


def set_regtest():
    global net
    net = BitcoinRegtest