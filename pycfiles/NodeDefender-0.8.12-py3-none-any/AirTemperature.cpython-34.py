# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/develop/NodeDefender/NodeDefender/icpe/zwave/commandclass/msensor/AirTemperature.py
# Compiled at: 2018-01-09 06:06:44
# Size of source mod 2**32: 651 bytes
import NodeDefender
fields = {'type': 'value',  'readonly': True,  'name': 'Celsius',  'web_field': True}
info = {'number': '1',  'name': 'AirTemperature',  'commandclass': 'msensor'}

def event(payload):
    data = {'commandclass': NodeDefender.icpe.zwave.commandclass.msensor.info,  'commandclasstype': info, 
     'fields': fields}
    if payload['unit'] == '1':
        return
    data['value'] = int(payload['data'], 0) / 10
    data['state'] = True if data['value'] else False
    data['icon'] = 'fa fa-thermometer-half'
    return data


def icon(value):
    return 'fa fa-thermometer-half'