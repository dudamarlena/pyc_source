# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: d:\Projects\Github\MobileHR\MobileHR.Mario.Engine\MobileHR.Mario.Engine\modules\net_state_modules\net_state_module.py
# Compiled at: 2018-12-10 13:03:31
# Size of source mod 2**32: 330 bytes
import socket

def get_net_state_info():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        result = s.getsockname()[0]
        s.close()
        return result
    except Exception as e:
        return str(e)