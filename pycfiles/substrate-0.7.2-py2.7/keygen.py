# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-intel/egg/substrate/data/lib/substrate/agar/keygen.py
# Compiled at: 2012-02-03 19:38:43
"""
The ``agar.keygen`` module contains functions for generating unique keys of various lengths.
"""
from uuid import uuid4
import basin

def _encode(bytes):
    return basin.encode('23456789abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ', basin.bytestring_to_integer(bytes))


def _gen_key(size=2):
    return ('').join(('').join(it) for it in zip(uuid4().bytes for _ in range(size)))


def gen_short_key():
    """
    Generates a short key (22 chars +/- 1) with a high probability of uniqueness
    """
    return _encode(_gen_key(size=1))


def gen_medium_key():
    """
    Generates a medium key (44 chars +/- 1) with a higher probability of uniqueness
    """
    return _encode(_gen_key(size=2))


def gen_long_key():
    """
    Generates a long key (66 chars +/- 1) with the highest probability of uniqueness
    """
    return _encode(_gen_key(size=3))


generate_key = gen_medium_key