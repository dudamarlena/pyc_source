# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\Crypto\pct_warnings.py
# Compiled at: 2013-03-13 13:15:35


class CryptoWarning(Warning):
    """Base class for PyCrypto warnings"""
    pass


class CryptoDeprecationWarning(DeprecationWarning, CryptoWarning):
    """Base PyCrypto DeprecationWarning class"""
    pass


class CryptoRuntimeWarning(RuntimeWarning, CryptoWarning):
    """Base PyCrypto RuntimeWarning class"""
    pass


class RandomPool_DeprecationWarning(CryptoDeprecationWarning):
    """Issued when Crypto.Util.randpool.RandomPool is instantiated."""
    pass


class ClockRewindWarning(CryptoRuntimeWarning):
    """Warning for when the system clock moves backwards."""
    pass


class GetRandomNumber_DeprecationWarning(CryptoDeprecationWarning):
    """Issued when Crypto.Util.number.getRandomNumber is invoked."""
    pass


class PowmInsecureWarning(CryptoRuntimeWarning):
    """Warning for when _fastmath is built without mpz_powm_sec"""
    pass


import warnings as _warnings
_warnings.filterwarnings('always', category=ClockRewindWarning, append=1)