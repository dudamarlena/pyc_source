# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/develop/NodeDefender/NodeDefender/config/logging.py
# Compiled at: 2018-03-20 10:55:30
import NodeDefender, os
default_config = {'enabled': False, 'level': 'DEBUG', 
   'engine': '', 
   'filepath': '', 
   'host': '', 
   'port': ''}
config = default_config.copy()

def load_config(parser):
    if eval(parser['LOGGING']['ENABLED']):
        config.update(parser['LOGGING'])
        config['enabled'] = True
    NodeDefender.app.config.update(LOGGING=config['enabled'], LOGGING_LEVEL=config['level'], LOGGING_ENGINE=config['engine'], LOGGING_FILEPATH=config['filepath'], LOGGING_HOST=config['host'], LOGGING_PORT=config['port'])
    return True


def set_default():
    config = default_config.copy()
    return True


def set(**kwargs):
    for key, value in kwargs.items():
        if key not in config:
            continue
        if key == 'filepath':
            value = os.path.join(NodeDefender.config.datafolder, value)
        config[key] = str(value)

    return True


def write():
    NodeDefender.config.parser['LOGGING'] = config
    NodeDefender.config.write()
    return True