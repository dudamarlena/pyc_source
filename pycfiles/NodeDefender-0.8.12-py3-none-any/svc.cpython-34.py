# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/develop/NodeDefender/NodeDefender/mqtt/message/respond/icpe/sys/svc.py
# Compiled at: 2018-01-09 06:06:44
# Size of source mod 2**32: 1214 bytes
import NodeDefender

def qry(topic, payload):
    telnet = bool(eval(payload.pop(0)))
    http = bool(eval(payload.pop(0)))
    snmp = bool(eval(payload.pop(0)))
    ssh = bool(eval(payload.pop(0)))
    return NodeDefender.db.icpe.update(topic['mac_address'], **{'telnet': telnet,  'http': http, 
     'snmp': snmp, 
     'ssh': ssh})


def cli(topic, payload):
    enabled = bool(eval(payload))
    return NodeDefender.db.icpe.update(topic['mac_address'], **{'telnet': telnet})


def web(topic, payload):
    enabled = bool(eval(payload))
    return NodeDefender.db.icpe.update(topic['mac_address'], **{'http': telnet})


def snmp(topic, payload):
    enabled = bool(eval(payload))
    return NodeDefender.db.icpe.update(topic['mac_address'], **{'snmp': telnet})


def ssh(topic, payload):
    enabled = bool(eval(payload))
    return NodeDefender.db.icpe.update(topic['mac_address'], **{'ssh': telnet})