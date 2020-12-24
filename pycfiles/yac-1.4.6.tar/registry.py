# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: yac/lib/registry.py
# Compiled at: 2017-11-16 20:28:41
import redis, shelve, os, fakeredis
from os.path import expanduser
from yac.lib.paths import get_config_path
PUBLIC_REGISTRY = {'host': 'pub-redis-15645.us-east-1-3.6.ec2.redislabs.com', 'port': 15645}
PRIVATE_REGISTRY_DB_KEY = 'private_registry'
MOCK_REGISTRY_HOST = 'MOCK'
MOCK_REGISTRY_DESC = {'host': MOCK_REGISTRY_HOST, 'port': 'n/a'}

class RegError:

    def __init__(self, msg):
        self.msg = msg


def _get_registry():
    private_registry = get_local_value(PRIVATE_REGISTRY_DB_KEY)
    if private_registry and 'host' in private_registry and private_registry['host'] != MOCK_REGISTRY_HOST:
        registry = redis.Redis(host=private_registry['host'], port=private_registry['port'])
    elif private_registry and 'host' in private_registry and private_registry['host'] == MOCK_REGISTRY_HOST:
        registry = fakeredis.FakeStrictRedis()
    else:
        registry = redis.Redis(host=PUBLIC_REGISTRY['host'], port=PUBLIC_REGISTRY['port'])
    return registry


def get_registry_keys():
    registry = _get_registry()
    return registry.keys()


def set_remote_string_w_challenge(key_name, string_value, challenge_phrase=''):
    original_challenge = ''
    already_registered = get_remote_value(key_name)
    if already_registered:
        original_challenge = _get_remote_challenge(key_name)
    if not challenge_phrase:
        challenge_phrase = raw_input('Enter your challenge phrase >> ')
    if not already_registered or challenge_phrase == original_challenge:
        value = {'challenge': challenge_phrase, 'value': string_value}
        registry = _get_registry()
        registry.hmset(key_name, value)
    else:
        print key_name, original_challenge
        raise RegError('challenge phrase mismatch')


def get_remote_value(key_name):
    registry = _get_registry()
    entry = registry.hgetall(key_name)
    if entry and type(entry) == dict:
        return entry['value']
    else:
        if entry:
            return entry
        return ''


def _get_remote_challenge(key_name):
    registry = _get_registry()
    entry = registry.hgetall(key_name)
    if entry:
        return entry['challenge']
    else:
        return ''


def clear_entry_w_challenge(key_name, challenge_phrase=''):
    original_challenge = ''
    already_registered = get_remote_value(key_name)
    if already_registered:
        original_challenge = _get_remote_challenge(key_name)
    if not challenge_phrase:
        challenge_phrase = raw_input('Enter your challenge phrase >> ')
    if not already_registered or challenge_phrase == original_challenge:
        _delete_registry_value(key_name)
    else:
        raise RegError('challenge phrase mismatch')


def _delete_registry_value(key_name):
    print 'clearing %s' % key_name
    registry = _get_registry()
    registry.delete(key_name)


def set_local_value(key_name, value):
    yac_db = _get_local_db()
    yac_db[key_name] = value


def get_local_value(key_name):
    local_db = _get_local_db()
    if key_name in local_db:
        return local_db[key_name]
    else:
        return ''


def delete_local_value(key_name):
    local_db = _get_local_db()
    if key_name in local_db:
        local_db.pop(key_name)


def get_local_keys():
    local_db = _get_local_db()
    return local_db.keys()


def set_private_registry(private_registry_desc):
    if private_registry_desc:
        print 'saving private registry setting'
        set_local_value(PRIVATE_REGISTRY_DB_KEY, private_registry_desc)


def get_private_registry():
    return get_local_value(PRIVATE_REGISTRY_DB_KEY)


def clear_private_registry():
    set_local_value(PRIVATE_REGISTRY_DB_KEY, {})


def _get_local_db():
    home = expanduser('~')
    db_home = os.path.join(home, '.yac')
    if not os.path.exists(db_home):
        os.makedirs(db_home)
    yac_db_path = os.path.join(db_home, 'yac_db')
    local_db = shelve.open(yac_db_path)
    return local_db