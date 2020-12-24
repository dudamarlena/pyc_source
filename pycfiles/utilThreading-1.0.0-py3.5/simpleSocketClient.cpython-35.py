# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/utilThreading/simpleSocketClient.py
# Compiled at: 2017-08-20 02:38:55
# Size of source mod 2**32: 1491 bytes
"""
------------------------------------------------------------------------------
Name:        simpleSocketClient
Author:      Sean Wiseman
------------------------------------------------------------------------------
"""
from socket import socket, AF_INET, SOCK_STREAM
__version__ = '1.0.0'

class SimpleSocketClient(object):

    def __init__(self, host, port, retry_count=3, buff_limit=4096):
        self.buff_limit = buff_limit
        self.host = host
        self.port = port
        self.retry_count = retry_count

    def send_by_socket(self, data):
        """ send pickled data via socket to target server """
        connected = False
        for retry in range(self.retry_count):
            if connected:
                break
            try:
                try:
                    sock_obj = socket(AF_INET, SOCK_STREAM)
                    sock_obj.connect((self.host, self.port))
                    connected = True
                except ConnectionRefusedError as err:
                    raise err

            finally:
                sock_obj.close()

        if connected:
            try:
                try:
                    sock_obj.sendall(data)
                    response = sock_obj.recv(self.buff_limit)
                    return response
                except (BrokenPipeError, TypeError) as err:
                    raise err

            finally:
                sock_obj.close()


if __name__ == '__main__':
    pass