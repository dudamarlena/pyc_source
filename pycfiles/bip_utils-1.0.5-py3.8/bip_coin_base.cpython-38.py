# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\bip_utils\bip_coin_base.py
# Compiled at: 2020-04-17 08:59:05
# Size of source mod 2**32: 4649 bytes
from .P2PKH import P2PKH
from .P2SH import P2SH
from .P2WPKH import P2WPKH
from .eth_addr import EthAddr
from .xrp_addr import XrpAddr

class BipCoinBase:
    __doc__ = " Bip coin base class. It's the base class for BipCoin classes (e.g. Bip44Coin, Bip49Coin).\n    It basically wraps the coin configuration allowing to get through methods.\n    "

    def __init__(self, coin_conf, key_net_ver, is_testnet, addr_fct):
        """ Construct class.

        Args:
            coin_conf (class)                  : Coin configuration class
            key_net_ver (KeyNetVersions object): Key net versions
            is_testnet (bool)                  : True if test net, false otherwise
            addr_fct (class)                   : Address class
        """
        self.m_coin_conf = coin_conf
        self.m_key_net_ver = key_net_ver
        self.m_is_testnet = is_testnet
        self.m_addr_fct = addr_fct

    def KeyNetVersions(self):
        """ Get key net versions.

        Returns:
            KeyNetVersions object: KeyNetVersions object
        """
        if not self.m_is_testnet:
            return self.m_key_net_ver.Main()
        return self.m_key_net_ver.Test()

    def WifNetVersion(self):
        """ Get WIF net version.

        Returns:
            bytes: WIF net version bytes
            None: If WIF is not supported
        """
        if not self.m_is_testnet:
            return self.m_coin_conf.WIF_NET_VER.Main()
        return self.m_coin_conf.WIF_NET_VER.Test()

    def IsTestNet(self):
        """ Get if test net

        Returns:
            bool: True if test net, false otherwise
        """
        return self.m_is_testnet

    def CoinNames(self):
        """ Get coin names.

        Returns:
            CoinNames object: CoinNames object
        """
        if not self.m_is_testnet:
            return self.m_coin_conf.NAMES
        return self.m_coin_conf.TEST_NAMES

    def ComputeAddress(self, pub_key):
        """ Compute address from public key.

        Args:
            pub_key (BipPublicKey object): BipPublicKey object

        Returns:
            str: Address string
        """
        if self.m_addr_fct is P2PKH:
            addr_ver = self.m_coin_conf.P2PKH_NET_VER.Main() if not self.m_is_testnet else self.m_coin_conf.P2PKH_NET_VER.Test()
            return self.m_addr_fct.ToAddress(pub_key.RawCompressed().ToBytes(), addr_ver)
        else:
            if self.m_addr_fct is P2SH:
                addr_ver = self.m_coin_conf.P2SH_NET_VER.Main() if not self.m_is_testnet else self.m_coin_conf.P2SH_NET_VER.Test()
                return self.m_addr_fct.ToAddress(pub_key.RawCompressed().ToBytes(), addr_ver)
            addr_ver = self.m_coin_conf.P2WPKH_NET_VER.Main() if self.m_addr_fct is P2WPKH and not self.m_is_testnet else self.m_coin_conf.P2WPKH_NET_VER.Test()
            return self.m_addr_fct.ToAddress(pub_key.RawCompressed().ToBytes(), addr_ver)
        if self.m_addr_fct is EthAddr:
            return self.m_addr_fct.ToAddress(pub_key.RawUncompressed().ToBytes())
        if self.m_addr_fct is XrpAddr:
            return self.m_addr_fct.ToAddress(pub_key.RawCompressed().ToBytes())
        raise RuntimeError('Invalid address class')