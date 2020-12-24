# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/guanpeixiang/Desktop/Project/canal-python/canal/connector.py
# Compiled at: 2019-09-25 02:48:41
import socket, struct

class Connector:
    sock = None
    packet_len = 4

    def connect(self, host, port, timeout=10):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.settimeout(timeout)
            self.sock.connect((host, port))
            self.sock.settimeout(None)
        except socket.error as e:
            print 'Connect to server error: %s' % e
            self.sock.close()

        return

    def disconnect(self):
        self.sock.close()

    def read(self, length):
        recv = ''
        while True:
            buf = self.sock.recv(length)
            if not buf:
                raise Exception('TSocket: Could not read bytes from server')
            read_len = len(buf)
            if read_len < length:
                recv = recv + buf
                length = length - read_len
            else:
                return recv + buf

    def write(self, buf):
        self.sock.sendall(buf)

    def read_next_packet(self):
        data = self.read(self.packet_len)
        data_len = struct.unpack('>i', data)
        return self.read(data_len[0])

    def write_with_header(self, data):
        self.write(struct.pack('>i', len(data)))
        self.write(data)