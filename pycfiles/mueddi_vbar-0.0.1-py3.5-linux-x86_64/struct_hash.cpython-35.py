# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mueddit/struct_hash.py
# Compiled at: 2019-04-19 02:32:55
# Size of source mod 2**32: 970 bytes
"""Naive Adler-32 hash computation for lists and dicts.

Specialized for the needs of Deterministic acyclic finite state
automata and Levenshtein automata in this package.
"""
MOD_ADLER = 65521

def hash_list(lst):
    """Hash (sorted) list, delegating to its members.

    Not suitable for general iterables (like set) because it expects
    same items in all lists to be in the same order.
    """
    a = 1
    b = 0
    for it in lst:
        a = (a + hash(it)) % MOD_ADLER
        b = (b + a) % MOD_ADLER

    return b << 16 | a


def hash_dict(d):
    """Hash dictionary with single-character keys and object values.

    Values are hashed by id, i.e. for equality using the is operator.
    """
    a = 1
    b = 0
    keys = sorted(d.keys())
    for k in keys:
        a = (a + ord(k)) % MOD_ADLER
        b = (b + a) % MOD_ADLER
        a = (a + id(d[k])) % MOD_ADLER
        b = (b + a) % MOD_ADLER

    return b << 16 | a