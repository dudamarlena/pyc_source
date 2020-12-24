# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_utils/protocol/tcp.py
# Compiled at: 2020-02-18 19:11:13
# Size of source mod 2**32: 902 bytes
"""PyAMS_utils.protocol.tcp module

This module only provides a single function, used to know if a given TCP port is already in use
"""
import socket
__docformat__ = 'restructuredtext'

def is_port_in_use(port, hostname='localhost'):
    """Check if given port is already used locally"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as (sock):
        return sock.connect_ex((hostname, port)) == 0