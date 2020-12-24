# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\bip_utils\bip84_coins.py
# Compiled at: 2020-04-17 08:47:51
# Size of source mod 2**32: 2523 bytes
from .bip_coin_base import BipCoinBase
from .bip_coin_conf import *
from .P2WPKH import P2WPKH

class Bip84Coin(BipCoinBase):
    __doc__ = ' Generic class for BIP-084 coins. '

    def __init__(self, coin_conf, is_testnet, addr_fct):
        super().__init__(coin_conf, coin_conf.BIP84_KEY_NET_VER, is_testnet, addr_fct)


Bip84BitcoinMainNet = Bip84Coin(coin_conf=BitcoinConf, is_testnet=False,
  addr_fct=P2WPKH)
Bip84BitcoinTestNet = Bip84Coin(coin_conf=BitcoinConf, is_testnet=True,
  addr_fct=P2WPKH)
Bip84LitecoinMainNet = Bip84Coin(coin_conf=LitecoinConf, is_testnet=False,
  addr_fct=P2WPKH)
Bip84LitecoinTestNet = Bip84Coin(coin_conf=LitecoinConf, is_testnet=True,
  addr_fct=P2WPKH)