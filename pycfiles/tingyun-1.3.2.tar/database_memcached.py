# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nb/publish/btw/tingyun/tingyun/armoury/database_memcached.py
# Compiled at: 2016-06-30 06:13:10
"""

"""
from tingyun.armoury.ammunition.memcache_tracker import wrap_memcache_trace
memcache_attr = {'add': {'path': 'Client.add', 'command': 'add'}, 'append': {'path': 'Client.append', 'command': 'append'}, 'cas': {'path': 'Client.cas', 'command': 'cas'}, 'decr': {'path': 'Client.decr', 'command': 'decr'}, 'delete': {'path': 'Client.delete', 'command': 'delete'}, 'delete_multi': {'path': 'Client.delete_multi', 'command': 'delete'}, 'get': {'path': 'Client.get', 'command': 'get'}, 'gets': {'path': 'Client.gets', 'command': 'get'}, 'get_multi': {'path': 'Client.get_multi', 'command': 'get'}, 'incr': {'path': 'Client.incr', 'command': 'incr'}, 'prepend': {'path': 'Client.prepend', 'command': 'prepend'}, 'replace': {'path': 'Client.replace', 'command': 'replace'}, 'set': {'path': 'Client.set', 'command': 'set'}, 'set_multi': {'path': 'Client.set_multi', 'command': 'set'}}

def detect(module):
    for attr in memcache_attr:
        if hasattr(module.Client, attr):
            wrap_memcache_trace(module, memcache_attr[attr]['path'], memcache_attr[attr]['command'])