# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/develop/NodeDefender/NodeDefender/mqtt/message/respond/icpe/sys/net.py
# Compiled at: 2018-01-09 06:06:44
# Size of source mod 2**32: 671 bytes
import NodeDefender

def set(topic, payload):
    return NodeDefender.mqtt.icpe.system_info(topic['mac_address'])


def qry(topic, payload):
    dhcp = bool(eval(payload.pop(0)))
    return NodeDefender.db.icpe.update(topic['mac_address'], **{'ip_dhcp': dhcp})


def stat(topic, payload):
    address = payload.pop(0)
    subnet = payload.pop(0)
    gateway = payload.pop(0)
    return NodeDefender.db.icpe.update(topic['mac_address'], **{'ip_address': address,  'ip_subnet': subnet, 
     'ip_gateway': gateway})