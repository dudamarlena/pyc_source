# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/develop/NodeDefender/NodeDefender/frontend/sockets/zwave.py
# Compiled at: 2018-01-09 06:06:44
# Size of source mod 2**32: 209 bytes
import NodeDefender

def event(mac_address, sensor_id, data):
    NodeDefender.socketio.emit('event', (mac_address, sensor_id, data), namespace='/icpe' + mac_address, broadcast=True)