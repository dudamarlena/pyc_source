# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/develop/NodeDefender/NodeDefender/mqtt/command/icpe/sys/network.py
# Compiled at: 2018-01-09 06:06:44
# Size of source mod 2**32: 506 bytes
from NodeDefender.mqtt.command import fire, topic_format

def set(mac_address, *args):
    topic = topic_format.format(mac_address, 'sys', 'net', 'set')
    payload = list(args)
    return fire(topic, payload=payload, icpe=mac_address)


def qry(mac_address):
    topic = topic_format.format(mac_address, 'sys', 'net', 'qry')
    return fire(topic, icpe=mac_address)


def stat(mac_address):
    topic = topic_format.format(mac_address, 'sys', 'net', 'stat')
    return fire(topic, icpe=mac_address)