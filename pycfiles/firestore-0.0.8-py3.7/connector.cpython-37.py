# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/firestore/db/connector.py
# Compiled at: 2019-08-25 22:19:11
# Size of source mod 2**32: 1263 bytes
import socket
GOOGLE_PUBLIC_DNS_A = '8.8.8.8'
GOOGLE_PUBLIC_DNS_TCP_PORT = 53
TIMEOUT = 3

def is_online(host=GOOGLE_PUBLIC_DNS_A, port=GOOGLE_PUBLIC_DNS_TCP_PORT, timeout=TIMEOUT):
    """
    Check if this machine is online as to determine if it is necessary to save to fs
    simulating cloud firestore
    """
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error:
        return False