# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/develop/NodeDefender/NodeDefender/mqtt/command/icpe/zwave/mode.py
# Compiled at: 2018-01-09 06:06:44
# Size of source mod 2**32: 335 bytes
from NodeDefender.mqtt.command import fire, topic_format

def include(mac_address):
    topic = topic_format.format(mac_address, '0', 'mode', 'include')
    return fire(topic, icpe=mac_address)


def exclude(mac_address):
    topic = topic_format.format(mac_address, '0', 'mode', 'exclude')
    return fire(topic, icpe=mac_address)