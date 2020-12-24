# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-qywz0dnj/ltk/ltk/check_connection.py
# Compiled at: 2019-11-20 16:41:05
# Size of source mod 2**32: 220 bytes
import socket

def check_for_connection():
    try:
        host = socket.gethostbyname('www.google.com')
        s = socket.create_connection((host, 80), 2)
        return True
    except:
        pass

    return False