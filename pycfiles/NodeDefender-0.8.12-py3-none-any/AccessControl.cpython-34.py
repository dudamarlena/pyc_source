# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/develop/NodeDefender/NodeDefender/icpe/zwave/commandclass/alarm/AccessControl.py
# Compiled at: 2018-01-09 06:06:44
# Size of source mod 2**32: 668 bytes
import NodeDefender
icons = {'16': 'fa fa-bell',  '17': 'fa fa-bell-slash-o',  '1': 'fa fa-bell', 
 '0': 'fa fa-bell-slash-o'}
fields = {'type': 'bool',  'readonly': True,  'name': 'Door/Window',  'web_field': True}
info = {'number': '06',  'name': 'AccessControl',  'commandclass': 'alarm'}

def event(payload):
    data = {'commandclass': NodeDefender.icpe.zwave.commandclass.alarm.info,  'commandclasstype': info, 
     'fields': fields}
    data['value'] = payload['evt']
    data['state'] = True if data['value'] == '16' else False
    data['icon'] = icons[data['value']]
    return data


def icon(value):
    return icons[value]