# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\bip_utils\bip_coin_conf_helper.py
# Compiled at: 2020-04-16 12:57:24
# Size of source mod 2**32: 3294 bytes
from . import utils

class CoinNames:
    __doc__ = ' Helper class for representing coin names. '

    def __init__(self, name, abbr):
        """ Construct class.

        Args:
            name (str): Name
            abbr (str): Abbreviation
        """
        self.m_name = name
        self.m_abbr = abbr

    def Name(self):
        """ Get name.

        Returns :
            str: Name
        """
        return self.m_name

    def Abbreviation(self):
        """ Get abbreviation.

        Returns:
            str: Abbreviation
        """
        return self.m_abbr


class KeyNetVersions:
    __doc__ = ' Helper class for representing key net versions. '

    def __init__(self, pub_net_ver, priv_net_ver):
        """ Construct class.

        Args:
            pub_net_ver (bytes) : Public net version
            priv_net_ver (bytes): Private net version
        """
        self.m_pub_net_ver = utils.HexStringToBytes(pub_net_ver)
        self.m_priv_net_ver = utils.HexStringToBytes(priv_net_ver)

    def Public(self):
        """ Get public net version.

        Returns:
            bytes: Public net version
        """
        return self.m_pub_net_ver

    def Private(self):
        """ Get private net version.

        Returns:
            bytes: Private net version
        """
        return self.m_priv_net_ver


class NetVersions:
    __doc__ = ' Helper class for representing net versions. '

    def __init__(self, main_net_ver=None, test_net_ver=None):
        """ Construct class.

        Args:
            main_net_ver (object): Main net version, None by default
            test_net_ver (object): Test net verions, None by default
        """
        self.m_main_net_ver = main_net_ver
        self.m_test_net_ver = test_net_ver

    def Main(self):
        """ Get main net version.

        Returns:
            object: Main net version
        """
        return self.m_main_net_ver

    def Test(self):
        """ Get test net version.

        Returns:
            object: Test net version
        """
        return self.m_test_net_ver