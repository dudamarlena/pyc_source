# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/develop/NodeDefender/NodeDefender/mqtt/command/sensor/parameter.py
# Compiled at: 2018-01-09 06:06:44
# Size of source mod 2**32: 704 bytes
import NodeDefender

def get(mac_address, sensor_id, number):
    topic = NodeDefender.mqtt.command.topic_format.format(mac_address, sensor_id, 'config', 'get')
    NodeDefender.mqtt.command.fire(topic, icpe=mac_address, payload=number)
    return True


def set(mac_address, sensor_id, number, size, value):
    topic = NodeDefender.mqtt.command.topic_format.format(mac_address, sensor_id, 'config', 'set')
    payload = number
    for x in range(int(size)):
        payload += ' 0 '

    payload += value
    NodeDefender.mqtt.command.fire(topic, icpe=mac_address, payload=payload)
    return True