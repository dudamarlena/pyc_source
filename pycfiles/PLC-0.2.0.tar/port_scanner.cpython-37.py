# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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