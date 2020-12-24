# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/toxiproxy/utils.py
# Compiled at: 2018-08-22 09:02:13
# Size of source mod 2**32: 259 bytes
import socket
from contextlib import closing

def can_connect_to(host, port):
    """ Test a connection to a host/port """
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as (sock):
        return bool(sock.connect_ex((host, port)) == 0)