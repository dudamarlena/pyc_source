# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dexstorebase/asset_permissions.py
# Compiled at: 2019-03-19 09:04:59
# Size of source mod 2**32: 1227 bytes
asset_permissions = {}
asset_permissions['charge_market_fee'] = 1
asset_permissions['white_list'] = 2
asset_permissions['override_authority'] = 4
asset_permissions['transfer_restricted'] = 8
asset_permissions['disable_force_settle'] = 16
asset_permissions['global_settle'] = 32
asset_permissions['disable_confidential'] = 64
asset_permissions['witness_fed_asset'] = 128
asset_permissions['committee_fed_asset'] = 256
whitelist = {}
whitelist['no_listing'] = 0
whitelist['white_listed'] = 1
whitelist['black_listed'] = 2
whitelist['white_and_black_listed'] = 3

def toint(permissions):
    permissions_int = 0
    for p in permissions:
        if permissions[p]:
            permissions_int |= asset_permissions[p]

    return permissions_int


def todict(number):
    r = {}
    for k, v in asset_permissions.items():
        r[k] = bool(number & v)

    return r


def force_flag(perms, flags):
    for p in flags:
        if flags[p]:
            perms |= asset_permissions[p]

    return perms


def test_permissions(perms, flags):
    for p in flags:
        if not asset_permissions[p] & perms:
            raise Exception('Permissions prevent you from changing %s!' % p)

    return True