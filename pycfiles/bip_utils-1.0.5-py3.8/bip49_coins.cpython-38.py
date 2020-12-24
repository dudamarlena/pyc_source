# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\bip_utils\bip49_coins.py
# Compiled at: 2020-04-17 08:47:51
# Size of source mod 2**32: 4712 bytes
from .bip_coin_base import BipCoinBase
from .bip_coin_conf import *
from .P2SH import P2SH

class Bip49Coin(BipCoinBase):
    __doc__ = ' Generic class for BIP-049 coins. '

    def __init__(self, coin_conf, is_testnet, addr_fct):
        super().__init__(coin_conf, coin_conf.BIP49_KEY_NET_VER, is_testnet, addr_fct)


class Bip49Litecoin(Bip49Coin):
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

    def ComputeAddress(self, pub_key):
        """ Compute address from public key.
        Litecoin overrides the method because it can have 2 different address versions.

        Args:
            pub_key (BipPublicKey object): BipPublicKey object

        Returns:
            str: Address string
        """
        p2sh_ver = self.m_coin_conf.P2SH_NET_VER if not self.m_coin_conf.P2SH_DEPR_ADDR else self.m_coin_conf.P2SH_DEPR_NET_VER
        addr_ver = p2sh_ver.Main() if not self.m_is_testnet else p2sh_ver.Test()
        return self.m_addr_fct.ToAddress(pub_key.RawCompressed().ToBytes(), addr_ver)


Bip49BitcoinMainNet = Bip49Coin(coin_conf=BitcoinConf, is_testnet=False,
  addr_fct=P2SH)
Bip49BitcoinTestNet = Bip49Coin(coin_conf=BitcoinConf, is_testnet=True,
  addr_fct=P2SH)
Bip49LitecoinMainNet = Bip49Litecoin(coin_conf=LitecoinConf, is_testnet=False,
  addr_fct=P2SH)
Bip49LitecoinTestNet = Bip49Litecoin(coin_conf=LitecoinConf, is_testnet=True,
  addr_fct=P2SH)
Bip49DogecoinMainNet = Bip49Coin(coin_conf=DogecoinConf, is_testnet=False,
  addr_fct=P2SH)
Bip49DogecoinTestNet = Bip49Coin(coin_conf=DogecoinConf, is_testnet=True,
  addr_fct=P2SH)
Bip49DashMainNet = Bip49Coin(coin_conf=DashConf, is_testnet=False,
  addr_fct=P2SH)
Bip49DashTestNet = Bip49Coin(coin_conf=DashConf, is_testnet=True,
  addr_fct=P2SH)