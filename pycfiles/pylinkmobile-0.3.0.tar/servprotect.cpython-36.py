# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pylinkirc/plugins/servprotect.py
# Compiled at: 2020-04-11 03:31:40
# Size of source mod 2**32: 1953 bytes
import threading
from pylinkirc import conf, utils
from pylinkirc.log import log
try:
    from cachetools import TTLCache
except ImportError:
    log.warning('servprotect: expiringdict support is deprecated as of PyLink 3.0; consider installing cachetools instead')
    from expiringdict import ExpiringDict as TTLCache

servprotect_conf = conf.conf.get('servprotect', {})
length = servprotect_conf.get('length', 10)
age = servprotect_conf.get('age', 10)

def _new_cache_dict():
    return TTLCache(length, age)


savecache = _new_cache_dict()
killcache = _new_cache_dict()
lock = threading.Lock()

def handle_kill(irc, numeric, command, args):
    """
    Tracks kills against PyLink clients. If too many are received,
    automatically disconnects from the network.
    """
    if args['userdata'] and irc.is_internal_server(args['userdata'].server) or irc.is_internal_client(args['target']):
        with lock:
            if killcache.setdefault(irc.name, 1) >= length:
                log.error('(%s) servprotect: Too many kills received, aborting!', irc.name)
                irc.disconnect()
            log.debug('(%s) servprotect: Incrementing killcache by 1', irc.name)
            killcache[irc.name] += 1


utils.add_hook(handle_kill, 'KILL')

def handle_save(irc, numeric, command, args):
    """
    Tracks SAVEs (nick collision) against PyLink clients. If too many are received,
    automatically disconnects from the network.
    """
    if irc.is_internal_client(args['target']):
        with lock:
            if savecache.setdefault(irc.name, 0) >= length:
                log.error('(%s) servprotect: Too many nick collisions, aborting!', irc.name)
                irc.disconnect()
            log.debug('(%s) servprotect: Incrementing savecache by 1', irc.name)
            savecache[irc.name] += 1


utils.add_hook(handle_save, 'SAVE')