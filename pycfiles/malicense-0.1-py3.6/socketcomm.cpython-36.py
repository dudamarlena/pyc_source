# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/malicense/socketcomm.py
# Compiled at: 2018-03-25 02:47:29
# Size of source mod 2**32: 1783 bytes
""" malicense.socketcomm.py """
import socket, time, sys

def sendMessage(hostname, port, message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (
     hostname, port)
    try:
        sock.connect(server_address)
        try:
            sock.sendall(message.encode())
        finally:
            sock.close()

    except:
        pass


timeFormat = '%Y-%m-%d.%H:%M:%S'

def startServer(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (
     '', port)
    print(('starting up on {} port {}'.format)(*server_address))
    sock.bind(server_address)
    sock.listen(1)
    while True:
        try:
            connection, client_address = sock.accept()
        except KeyboardInterrupt:
            sys.exit(0)

        client_ip, client_port = client_address
        access_time = time.gmtime()
        try:
            full_data = ''
            while True:
                try:
                    data = connection.recv(16).decode()
                except:
                    full_data += '...CORRUPTED'
                    break

                if data:
                    full_data += data
                else:
                    break

        finally:
            connection.close()

        accInfo = (
         time.strftime(timeFormat, access_time), client_ip, full_data)
        yield accInfo