# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/develop/NodeDefender/NodeDefender/config/redis.py
# Compiled at: 2018-03-20 10:59:17
import NodeDefender
default_config = {'enabled': False, 'host': '', 
   'port': '', 
   'database': ''}
config = default_config.copy()

def load_config(parser):
    if eval(parser['REDIS']['ENABLED']):
        config.update(parser['REDIS'])
        config['enabled'] = True
    NodeDefender.app.config.update(REDIS=config['enabled'], REDIS_HOST=config['host'], REDIS_PORT=config['port'], REDIS_DATABASE=config['database'])
    return True


def set_default():
    config = default_config.copy()


def set(**kwargs):
    for key, value in kwargs.items():
        if key not in config:
            continue
        NodeDefender.config.redis.config[key] = str(value)

    return True


def write():
    NodeDefender.config.parser['REDIS'] = config
    return NodeDefender.config.write()