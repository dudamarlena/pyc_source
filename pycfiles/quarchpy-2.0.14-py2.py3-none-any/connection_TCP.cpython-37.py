# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\sboon\AppData\Local\Temp\pip-install-ptdbtr91\quarchpy\quarchpy\connection_specific\connection_TCP.py
# Compiled at: 2020-03-25 05:10:07
# Size of source mod 2**32: 1993 bytes
import time, socket, sys, select

class TCPConn:

    def __init__(self, ConnTarget):
        TCP_PORT = 9760
        self.ConnTarget = ConnTarget
        self.Connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.BufferSize = 4096
        self.Connection.connect((self.ConnTarget, TCP_PORT))

    def close(self):
        self.Connection.close()
        return True

    def sendCommand(self, Command, readUntilCursor=True, expectedResponse=True):
        time.sleep(0.015)
        MESSAGE_ready = (chr(len(Command + '\r\n')) + chr(0) + Command + '\r\n').encode()
        self.Connection.send(MESSAGE_ready)
        if expectedResponse == True:
            if sys.version_info >= (3, 0):
                packet = self.Connection.recv(self.BufferSize)
                messageLength = packet[0] + packet[1] * 256
                data = packet[2:]
                while len(data) < messageLength:
                    packet = self.Connection.recv(self.BufferSize)
                    data = data + packet

                data = data.decode()
                data = data.strip('> \t\n\r')
            else:
                data_raw = self.Connection.recv(self.BufferSize)
                data = data_raw.decode('ISO-8859-1')[1:-3]
            return data
        return