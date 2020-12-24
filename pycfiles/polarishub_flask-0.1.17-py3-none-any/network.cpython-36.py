# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/david/flask_proj/polarishub_flask/polarishub_flask/server/network.py
# Compiled at: 2019-08-27 21:47:35
# Size of source mod 2**32: 630 bytes
import socket
from polarishub_flask.server.parser import printv
host_ip = None

def get_host_ip():
    global host_ip
    if host_ip is not None:
        return host_ip
    else:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 80))
            host_ip = s.getsockname()[0]
        finally:
            s.close()

        return host_ip


def checkIP(addr):
    return addr == '127.0.0.1'