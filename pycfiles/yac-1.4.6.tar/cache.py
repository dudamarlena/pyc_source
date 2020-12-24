# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/x0ox/Dropbox/ActiveDev/yac/yac/lib/cache.py
# Compiled at: 2017-11-16 20:28:41
import shelve, os, sys, time, datetime
from yac.lib.paths import get_config_path

class CacheError:

    def __init__(self, msg):
        self.msg = msg


def set_cache_value_ms(key_name, value, expiration_ms=''):
    yac_db = _get_cache()
    if not expiration_ms:
        expiration_dt = datetime.date.today() + datetime.timedelta(days=365)
        expiration_ms = int(expiration_dt.strftime('%s')) * 1000
    yac_db[key_name] = {'value': value, 'expiration_ms': expiration_ms}


def set_cache_value_dt(key_name, value, expiration_dt=''):
    yac_db = _get_cache()
    if not expiration_dt:
        expiration_dt = datetime.date.today() + datetime.timedelta(days=365)
    expiration_ms = int(expiration_dt.strftime('%s')) * 1000
    yac_db[key_name] = {'value': value, 'expiration_ms': expiration_ms}


def get_cache_value(key_name, default_value={}):
    cache_db = _get_cache()
    time_ms = int(time.time() * 1000)
    if key_name in cache_db and time_ms < cache_db[key_name]['expiration_ms']:
        return cache_db[key_name]['value']
    else:
        return default_value


def delete_cache_value(key_name):
    cache_db = _get_cache()
    if key_name in cache_db:
        cache_db.pop(key_name)


def get_cache_keys():
    cache_db = _get_cache()
    return cache_db.keys()


def _get_cache():
    home = os.path.expanduser('~')
    db_home = os.path.join(home, '.yac')
    if not os.path.exists(db_home):
        os.makedirs(db_home)
    yac_db_path = os.path.join(db_home, 'yac_cache')
    cache_db = shelve.open(yac_db_path)
    return cache_db