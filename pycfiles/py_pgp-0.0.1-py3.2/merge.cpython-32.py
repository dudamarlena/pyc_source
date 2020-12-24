# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pgp/merge.py
# Compiled at: 2015-08-31 08:17:33
from collections import OrderedDict
from pgp import utils

def keys_equivalent(key1, key2):
    return key1.version == key2.version and key1.public_key_algorithm == key2.public_key_algorithm and key1.modulus_n == key2.modulus_n and key1.exponent_e == key2.exponent_e and key1.prime_p == key2.prime_p and key1.group_generator_g == key2.group_generator_g and key1.group_order_q == key2.group_order_q and key1.key_value_y == key2.key_value_y and key1.creation_time == key2.creation_time


def merge_sigpairs(parts):
    m = OrderedDict()
    for part in parts:
        old_sigs = m.setdefault(part, [])
        for sig in part.signatures:
            sig_key = signature_key(sig)
            for sig2 in old_sigs:
                sig_key2 = signature_key(sig2)
                if sig_key != sig_key2:
                    old_sigs.append(sig)
                    continue

    for part, sigs in m.items():
        part.signatures = []
        selfsig = None
        for sig in sigs:
            if sig.is_self_signature() and selfsig:
                if sig.creation_time > selfsig.creation_time:
                    selfsig = sig
            else:
                part.signatures.append(sig)

        part.signatures.insert(0, selfsig)

    return


def merge_sigpair_lists(part1, part2):
    return merge_sigpairs(part1 + part2)


_marker = object()

def signature_key(sig):
    return (
     sig.version,
     sig.signature_type,
     sig.public_key_algorithm,
     sig.hash_algorithm,
     sig.creation_time,
     set(sig.issuer_key_ids))


def merge(key, candidate_key):
    if not keys_equivalent(key, candidate_key):
        return key
    signatures = candidate_key.signatures
    old_sigs = OrderedDict()
    for sig in signatures:
        sig_key = signature_key(sig)
        for sig2 in old_sigs:
            sig_key2 = signature_key(sig2)
            if sig_key == sig_key2:
                break
        else:
            old_sigs[sig_key] = sig

    old_user_ids = candidate_key.user_ids
    old_user_attributes = candidate_key.user_attributes
    old_subkeys = candidate_key.subkeys
    for sig in old_sigs.values():
        if sig not in key.signatures:
            key.signatures.append(sig)
            continue

    key.user_ids = merge_sigpair_lists(key.user_ids, old_user_ids)
    key.user_attributes = merge_sigpair_lists(key.user_attributes, old_user_attributes)
    key.subkeys = merge_sigpair_lists(key.subkeys, old_subkeys)
    return key


def merge_key(key, db):
    key_id = key.key_id
    if hasattr(db, 'get_key_by_hash'):
        if db.get_key_by_hash(utils.hash_entire_key(key)):
            return key
    potential_merges = list(db.search(key_id=key_id))
    if potential_merges:
        key = merge(key, potential_merges[0])
    return key