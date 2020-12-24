# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/develop/NodeDefender/NodeDefender/mqtt/message/respond/sensor/info.py
# Compiled at: 2018-01-09 06:06:44
# Size of source mod 2**32: 485 bytes
import NodeDefender

def qry(topic, payload):
    return NodeDefender.icpe.sensor.sensor_info(topic['mac_address'], topic['node'], **payload)


def sup(topic, payload):
    if type(payload) is not dict:
        return True
    return NodeDefender.icpe.sensor.commandclass.commandclass_types(topic['mac_address'], topic['node'], topic['commandClass'], **payload)


def evtsup(topic, payload):
    return True