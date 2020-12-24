# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/electrum_chi/electrum/version.py
# Compiled at: 2019-08-24 06:06:43
# Size of source mod 2**32: 784 bytes
ELECTRUM_VERSION = '3.3.8'
APK_VERSION = '3.3.8.0'
PROTOCOL_VERSION = '1.4.1'
SEED_PREFIX = '01'
SEED_PREFIX_SW = '100'
SEED_PREFIX_2FA = '101'
SEED_PREFIX_2FA_SW = '102'

def seed_prefix(seed_type):
    if seed_type == 'standard':
        return SEED_PREFIX
    if seed_type == 'segwit':
        return SEED_PREFIX_SW
    if seed_type == '2fa':
        return SEED_PREFIX_2FA
    if seed_type == '2fa_segwit':
        return SEED_PREFIX_2FA_SW
    raise Exception(f"unknown seed_type: {seed_type}")