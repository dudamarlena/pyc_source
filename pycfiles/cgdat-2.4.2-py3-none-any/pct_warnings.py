# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cgcloud_Crypto/pct_warnings.py
# Compiled at: 2016-11-22 15:21:45


class CryptoWarning(Warning):
    """Base class for PyCrypto warnings"""


class CryptoDeprecationWarning(DeprecationWarning, CryptoWarning):
    """Base PyCrypto DeprecationWarning class"""


class CryptoRuntimeWarning(RuntimeWarning, CryptoWarning):
    """Base PyCrypto RuntimeWarning class"""


class RandomPool_DeprecationWarning(CryptoDeprecationWarning):
    """Issued when Crypto.Util.randpool.RandomPool is instantiated."""


class ClockRewindWarning(CryptoRuntimeWarning):
    """Warning for when the system clock moves backwards."""


class GetRandomNumber_DeprecationWarning(CryptoDeprecationWarning):
    """Issued when Crypto.Util.number.getRandomNumber is invoked."""


class DisableShortcut_DeprecationWarning(CryptoDeprecationWarning):
    """Issued when Counter.new(disable_shortcut=...) is invoked."""


class PowmInsecureWarning(CryptoRuntimeWarning):
    """Warning for when _fastmath is built without mpz_powm_sec"""


import warnings as _warnings
_warnings.filterwarnings('always', category=ClockRewindWarning, append=1)