# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/develop/NodeDefender/NodeDefender/config/celery.py
# Compiled at: 2018-03-19 08:40:05
import NodeDefender
default_config = {'enabled': False, 'broker': '', 
   'host': '', 
   'port': '', 
   'database': '', 
   'server_name': ''}
config = default_config.copy()

def load_config(parser):
    if eval(parser['CELERY']['ENABLED']):
        config.update(parser['CELERY'])
        config['enabled'] = True
    NodeDefender.app.config.update(CELERY=config['enabled'])
    if config['enabled']:
        NodeDefender.app.config.update(CELERY_BROKER=config['broker'], CELERY_HOST=config['host'], CELERY_PORT=config['port'], CELERY_DATABASE=config['database'], SERVER_NAME=config['server_name'])
    return True


def broker_uri():
    server = config['server']
    port = config['port']
    database = config['database']
    if config['broker'] == 'REDIS':
        return 'redis://' + server + ':' + port + '/' + database
    else:
        if config['broker'] == 'AMQP':
            return 'pyamqp://' + server + ':' + port + '/' + database
        return


def set_default():
    config = default_config.copy()
    return True


def set(**kwargs):
    for key, value in kwargs.items():
        if key not in config:
            continue
        NodeDefender.config.celery.config[key] = str(value)

    return True


def write():
    NodeDefender.config.parser['CELERY'] = config
    NodeDefender.config.write()