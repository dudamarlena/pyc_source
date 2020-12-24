# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_utils/protocol/tcp.py
# Compiled at: 2020-02-18 19:11:13
# Size of source mod 2**32: 902 bytes
__doc__ = 'PyAMS_utils.protocol.tcp module\n\nThis module only provides a single function, used to know if a given TCP port is already in use\n'
import socket
__docformat__ = 'restructuredtext'

def is_port_in_use(port, hostname='localhost'):
    """Check if given port is already used locally"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as (sock):
        return sock.connect_ex((hostname, port)) == 0