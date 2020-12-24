# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\bip_utils\bip_coin_conf.py
# Compiled at: 2020-04-16 12:59:51
# Size of source mod 2**32: 7036 bytes
from .bip_coin_conf_helper import *

class Bip32Conf:
    __doc__ = ' Class container for Bip32 configuration. '
    KEY_NET_VER = NetVersions(KeyNetVersions(b'0488b21e', b'0488ade4'), KeyNetVersions(b'043587cf', b'04358394'))


class BitcoinConf:
    __doc__ = ' Class container for Bitcoin configuration. '
    NAMES = CoinNames('Bitcoin', 'BTC')
    TEST_NAMES = CoinNames('Bitcoin TestNet', 'BTC')
    BIP44_KEY_NET_VER = Bip32Conf.KEY_NET_VER
    BIP49_KEY_NET_VER = NetVersions(KeyNetVersions(b'049d7cb2', b'049d7878'), KeyNetVersions(b'044a5262', b'044a4e28'))
    BIP84_KEY_NET_VER = NetVersions(KeyNetVersions(b'04b24746', b'04b2430c'), KeyNetVersions(b'045f1cf6', b'045f18bc'))
    P2PKH_NET_VER = NetVersions(b'\x00', b'o')
    P2SH_NET_VER = NetVersions(b'\x05', b'\xc4')
    P2WPKH_NET_VER = NetVersions('bc', 'tb')
    WIF_NET_VER = NetVersions(b'\x80', b'\xef')


class LitecoinConf:
    __doc__ = ' Class container for Litecoin configuration. '
    NAMES = CoinNames('Litecoin', 'LTC')
    TEST_NAMES = CoinNames('Litecoin TestNet', 'LTC')
    EX_KEY_ALT = False
    P2SH_DEPR_ADDR = False
    BIP44_KEY_NET_VER = NetVersions((BitcoinConf.BIP44_KEY_NET_VER.Main(), KeyNetVersions(b'019da462', b'019d9cfe')), KeyNetVersions(b'0436f6e1', b'0436ef7d'))
    BIP49_KEY_NET_VER = NetVersions((BitcoinConf.BIP49_KEY_NET_VER.Main(), KeyNetVersions(b'01b26ef6', b'01b26792')), KeyNetVersions(b'0436f6e1', b'0436ef7d'))
    BIP84_KEY_NET_VER = NetVersions(BitcoinConf.BIP84_KEY_NET_VER.Main(), KeyNetVersions(b'0436f6e1', b'0436ef7d'))
    P2PKH_NET_VER = NetVersions(b'0', b'o')
    P2SH_DEPR_NET_VER = BitcoinConf.P2SH_NET_VER
    P2SH_NET_VER = NetVersions(b'2', b':')
    P2WPKH_NET_VER = NetVersions('ltc', 'tltc')
    WIF_NET_VER = NetVersions(b'\xb0', b'\xef')


class DogecoinConf:
    __doc__ = ' Class container for Dogecoin configuration. '
    NAMES = CoinNames('Dogecoin', 'DOGE')
    TEST_NAMES = CoinNames('Dogecoin TestNet', 'DOGE')
    BIP44_KEY_NET_VER = NetVersions(KeyNetVersions(b'02facafd', b'02fac398'), KeyNetVersions(b'0432a9a8', b'0432a243'))
    BIP49_KEY_NET_VER = NetVersions(KeyNetVersions(b'02facafd', b'02fac398'), KeyNetVersions(b'0432a9a8', b'0432a243'))
    P2PKH_NET_VER = NetVersions(b'\x1e', b'q')
    P2SH_NET_VER = NetVersions(b'\x16', b'\xc4')
    WIF_NET_VER = NetVersions(b'\x9e', b'\xf1')


class DashConf:
    __doc__ = ' Class container for Dash configuration. '
    NAMES = CoinNames('Dash', 'DASH')
    TEST_NAMES = CoinNames('Dash TestNet', 'DASH')
    BIP44_KEY_NET_VER = BitcoinConf.BIP44_KEY_NET_VER
    BIP49_KEY_NET_VER = BitcoinConf.BIP49_KEY_NET_VER
    P2PKH_NET_VER = NetVersions(b'L', b'\x8c')
    P2SH_NET_VER = NetVersions(b'\x10', b'\x13')
    WIF_NET_VER = NetVersions(b'\xcc', b'\xef')


class EthereumConf:
    __doc__ = ' Class container for Ethereum configuration. '
    NAMES = CoinNames('Ethereum', 'ETH')
    BIP44_KEY_NET_VER = BitcoinConf.BIP44_KEY_NET_VER
    WIF_NET_VER = NetVersions()


class RippleConf:
    __doc__ = ' Class container for Bitcoin configuration. '
    NAMES = CoinNames('Ripple', 'XRP')
    BIP44_KEY_NET_VER = BitcoinConf.BIP44_KEY_NET_VER
    P2PKH_NET_VER = NetVersions(b'\x00')
    WIF_NET_VER = NetVersions()