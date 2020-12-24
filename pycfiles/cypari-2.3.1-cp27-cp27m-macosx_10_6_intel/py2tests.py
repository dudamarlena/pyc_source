# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dunfield/cypari/Version2/build/lib.macosx-10.6-intel-2.7/cypari/py2tests.py
# Compiled at: 2020-03-01 20:27:02
"""
Tests specific to Python 2:

    >>> old_prec = pari.set_real_precision(63)
    >>> int(pari('2^63-1'))
    9223372036854775807L  # 32-bit
    9223372036854775807   # 64-bit
    >>> int(pari('2^63+2')))
    9223372036854775810L
    >>> pari.set_real_precision(old_prec)
    >>> print(hex(pari(0)))
    0
    >>> print(hex(pari(15)))
    f
    >>> print(hex(pari(16)))
    10
    >>> print(hex(pari(16938402384092843092843098243)))
    36bb1e3929d1a8fe2802f083
    >>> print(hex(pari(-16938402384092843092843098243)))
    -36bb1e3929d1a8fe2802f083
"""