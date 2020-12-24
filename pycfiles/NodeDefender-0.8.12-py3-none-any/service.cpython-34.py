# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/develop/NodeDefender/NodeDefender/mqtt/command/icpe/sys/service.py
# Compiled at: 2018-01-09 06:06:44
# Size of source mod 2**32: 889 bytes
from NodeDefender.mqtt.command import fire, topic_format

def qry(mac_address):
    topic = topic_format.format(mac_address, 'sys', 'svc', 'qry')
    return fire(topic, icpe=mac_address)


def telnet(mac_address, enabled):
    topic = topic_format.format(mac_address, 'sys', 'svc:cli', 'set')
    return fire(topic, payload=str(int(enabled)), icpe=mac_address)


def ssh(mac_address, enabled):
    topic = topic_format.format(mac_address, 'sys', 'svc:ssh', 'set')
    return fire(topic, payload=str(int(enabled)), icpe=mac_address)


def web(mac_address, enabled):
    topic = topic_format.format(mac_address, 'sys', 'svc:web', 'st')
    return fire(topic, payload=str(int(enabled)), icpe=mac_address)


def snmp(mac_address, enabled):
    topic = topic_format.format(mac_address, 'sys', 'svc:snmp', 'set')
    return fire(topic, payload=str(int(enabled)), icpe=mac_address)