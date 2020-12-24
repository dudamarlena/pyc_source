# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fsuba/Pictures/plbmng-0.3.7/plbmng/lib/port_scanner.py
# Compiled at: 2019-04-30 03:47:16
# Size of source mod 2**32: 715 bytes
import socket, sys

def testPortAvailability(hostname, port):
    try:
        server_ip = socket.gethostbyname(hostname)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((server_ip, port))
        if result == 0:
            return True
        return False
        sock.close()
    except KeyboardInterrupt:
        print('You pressed Ctrl+C')
        sys.exit(96)
    except socket.gaierror:
        return 98
    except socket.error:
        return 97