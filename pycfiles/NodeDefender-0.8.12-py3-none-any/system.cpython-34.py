# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/develop/NodeDefender/NodeDefender/icpe/system.py
# Compiled at: 2018-01-09 06:06:44
# Size of source mod 2**32: 818 bytes
import NodeDefender

def system_info(mac_address, **info):
    if info:
        NodeDefender.db.icpe.update(mac_address, **info)
    icpe = NodeDefender.db.icpe.get(mac_address)
    return {'mac_address': icpe['mac_address'],  'serialNumber': icpe['serialNumber'], 
     'hardware': icpe['hardware'], 
     'software': icpe['software']}


def network_settings(mac_address, **settings):
    if settings:
        NodeDefender.db.icpe.update(mac_address, **settings)
    icpe = NodeDefender.db.icpe.get(mac_address)
    return {'ipDhcp': icpe['ip_dhcp'],  'ipAddress': icpe['ip_address'], 
     'ipSubnet': icpe['ip_subnet'], 
     'ipGateway': icpe['ip_gateway']}


def time_settings(mac_address, **settings):
    pass


def battery_info(mac_address, **info):
    pass