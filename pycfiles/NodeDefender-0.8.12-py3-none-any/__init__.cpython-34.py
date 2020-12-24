# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/develop/NodeDefender/NodeDefender/mqtt/__init__.py
# Compiled at: 2018-01-14 09:42:59
# Size of source mod 2**32: 314 bytes
import logging, NodeDefender.mqtt.message, NodeDefender.mqtt.command
from NodeDefender.mqtt import connection
logger = logging.getLogger(__name__)
logger.setLevel('DEBUG')

def load(loggHandler):
    logger.addHandler(loggHandler)
    connection.load()
    logger.debug('MQTT Loaded')
    return True