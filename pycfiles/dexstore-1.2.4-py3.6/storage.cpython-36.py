# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dexstore/storage.py
# Compiled at: 2019-03-24 13:23:53
# Size of source mod 2**32: 750 bytes
from graphenestorage import InRamConfigurationStore, InRamEncryptedKeyStore, InRamPlainKeyStore, SqliteConfigurationStore, SqliteEncryptedKeyStore, SQLiteFile, SqlitePlainKeyStore
url = 'ws://127.0.0.1:7738'
SqliteConfigurationStore.setdefault('node', url)
SqliteConfigurationStore.setdefault('order-expiration', 30758400)

def get_default_config_store(*args, **kwargs):
    if 'appname' not in kwargs:
        kwargs['appname'] = 'dexstore'
    return SqliteConfigurationStore(*args, **kwargs)


def get_default_key_store(config, *args, **kwargs):
    if 'appname' not in kwargs:
        kwargs['appname'] = 'dexstore'
    return SqliteEncryptedKeyStore(config=config, **kwargs)