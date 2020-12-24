# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/develop/NodeDefender/NodeDefender/manage/setup/redis.py
# Compiled at: 2018-03-09 03:40:48
# Size of source mod 2**32: 1468 bytes
from NodeDefender.manage.setup import manager, print_message, print_topic, print_info
from flask_script import prompt
import NodeDefender

@manager.command
def redis():
    print_topic('Redis')
    print_info('Redis is used to store temporary data(Current heat of sensor               etc). With redis enabled it will store the data in Redis.               Disabled will store in as a local class- object')
    enabled = None
    while enabled is None:
        enabled = prompt('Enable Redis(Y/N)').upper()
        if 'Y' in enabled:
            enabled = True
        elif 'N' in enabled:
            enabled = False
        else:
            enabled = None

    if not enabled:
        NodeDefender.config.redis.set(enabled=False)
        if NodeDefender.config.redis.write():
            print_info('Redis- config successfully written')
        return True
    host = None
    while host is None:
        host = prompt('Enter Host Address')

    port = None
    while port is None:
        port = prompt('Enter Server Port')

    database = ''
    while not database:
        database = prompt('Enter Database')

    NodeDefender.config.redis.set(enabled=True, host=host, port=port, database=database)
    if NodeDefender.config.redis.write():
        print_info('Redis- config successfully written')
    return True