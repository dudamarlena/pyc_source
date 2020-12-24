# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/c/Users/dave/Projects/Github/proxenos/src/proxenos/rendezvous.py
# Compiled at: 2017-01-21 18:51:58
# Size of source mod 2**32: 2031 bytes
"""Provides node selection based on Highest Random Weight (HRW) hashing."""
from __future__ import absolute_import
import codecs, hashlib, random, struct, sys, typing, mmh3, six, proxenos.node
__all__ = ('select_node', 'weight')
ARCH = struct.calcsize('P') * 8
HashCallback = typing.Callable[([typing.Any, int], int)]

def murmur_128(key, seed=0):
    return mmh3.hash128(key, seed=seed, x64arch=(ARCH == 64))


def srand(seed=0):
    if isinstance(seed, (bytes, six.string_types)):
        if isinstance(seed, six.text_type):
            seed = seed.encode()
        seed_int = int(codecs.encode(hashlib.sha512(seed).digest(), 'hex'), 16)
        print(seed_int)
        seed = typing.cast(int, seed_int)
    rng = random.Random(seed)
    while True:
        yield rng.randint(0, sys.maxsize)


def select_node(cluster, key, hash_fn=None, hash_seed=0):
    """Selects a node from the given cluster based using HRW hashing."""
    max_weight = 0
    selected_node = None
    for node in cluster:
        node_weight = weight(node, key, hash_fn, hash_seed)
        if node_weight > max_weight:
            max_weight = node_weight
            selected_node = node

    return selected_node


def weight(socket_address, key, hash_fn=None, hash_seed=0):
    if hash_fn is None:
        hash_fn = murmur_128
    seed = next(srand(socket_address.pack()))
    digest = hash_fn(key, hash_seed)
    return next(srand(seed ^ digest))