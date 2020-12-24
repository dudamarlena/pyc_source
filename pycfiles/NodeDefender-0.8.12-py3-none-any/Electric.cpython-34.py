# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/develop/NodeDefender/NodeDefender/icpe/zwave/commandclass/meter/Electric.py
# Compiled at: 2018-01-09 06:06:44
# Size of source mod 2**32: 537 bytes
import NodeDefender
fields = {'type': 'value',  'readonly': True,  'name': 'Watt',  'web_field': True}
info = {'name': 'Electric',  'number': '1',  'commandclass': 'meter'}

def icon(value):
    return 'fa fa-plug'


def event(payload):
    data = {'commandclass': NodeDefender.icpe.zwave.commandclass.meter.info,  'commandclasstype': info, 
     'fields': fields}
    data['value'] = int(payload['data'], 0)
    data['state'] = True if data['value'] > 1.0 else False
    data['icon'] = 'fa fa-plug'
    return data