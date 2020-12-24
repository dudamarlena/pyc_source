# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\bip_utils\bip44_coins.py
# Compiled at: 2020-04-17 08:47:51
# Size of source mod 2**32: 4539 bytes
from .bip_coin_base import BipCoinBase
from .bip_coin_conf import *
from .P2PKH import P2PKH
from .eth_addr import EthAddr
from .xrp_addr import XrpAddr

class Bip44Coin(BipCoinBase):
    __doc__ = ' Generic class for BIP-044 coins. '

    def __init__(self, coin_conf, is_testnet, addr_fct):
        super().__init__(coin_conf, coin_conf.BIP44_KEY_NET_VER, is_testnet, addr_fct)


class Bip44Litecoin(Bip44Coin):
    __doc__ = ' Litecoin BIP-0044 class.\n    It overrides KeyNetVersions to return different main net versions depending on the configuration.\n    '

    def KeyNetVersions(self):
        """ Get key net versions. It overrides the method in BipCoinBase.
        Litecoin overrides the method because it can have 2 different main net versions.

        Returns:
            KeyNetVersions object: KeyNetVersions object
        """
        if not self.m_is_testnet:
            if not self.m_coin_conf.EX_KEY_ALT:
                return self.m_key_net_ver.Main()[0]
            return self.m_key_net_ver.Main()[1]
        return self.m_key_net_ver.Test()


Bip44BitcoinMainNet = Bip44Coin(coin_conf=BitcoinConf, is_testnet=False,
  addr_fct=P2PKH)
Bip44BitcoinTestNet = Bip44Coin(coin_conf=BitcoinConf, is_testnet=True,
  addr_fct=P2PKH)
Bip44LitecoinMainNet = Bip44Litecoin(coin_conf=LitecoinConf, is_testnet=False,
  addr_fct=P2PKH)
Bip44LitecoinTestNet = Bip44Litecoin(coin_conf=LitecoinConf, is_testnet=True,
  addr_fct=P2PKH)
Bip44DogecoinMainNet = Bip44Coin(coin_conf=DogecoinConf, is_testnet=False,
  addr_fct=P2PKH)
Bip44DogecoinTestNet = Bip44Coin(coin_conf=DogecoinConf, is_testnet=True,
  addr_fct=P2PKH)
Bip44DashMainNet = Bip44Coin(coin_conf=DashConf, is_testnet=False,
  addr_fct=P2PKH)
Bip44DashTestNet = Bip44Coin(coin_conf=DashConf, is_testnet=True,
  addr_fct=P2PKH)
Bip44Ethereum = Bip44Coin(coin_conf=EthereumConf, is_testnet=False,
  addr_fct=EthAddr)
Bip44Ripple = Bip44Coin(coin_conf=RippleConf, is_testnet=False,
  addr_fct=XrpAddr)