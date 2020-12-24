# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: d:\shared\tim_working\development\github\pylirious\pylirious\mm-api\distrib\python\mmRemote.py
# Compiled at: 2016-07-24 13:10:59
import mmapi, struct, socket, array

class mmRemote:

    def __init__(self):
        self.address = '127.0.0.1'
        self.receive_port = 45023
        self.send_port = 45007
        self.debug_print = False

    def connect(self):
        self.send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.receive_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.receive_sock.bind((self.address, self.receive_port))

    def shutdown(self):
        self.send_sock.close()
        self.receive_sock.close()

    def runCommand(self, cmd):
        serializer = mmapi.BinarySerializer()
        cmd.Store(serializer)
        commandBuf = serializer.buffer()
        sendBuf = array.array('B', commandBuf)
        if self.debug_print:
            print '[mmRemote::runCommand] sending...'
        self.send_sock.sendto(sendBuf, (self.address, self.send_port))
        if self.debug_print:
            print '[mmRemote::runCommand] waiting for response...'
        data, addr = self.receive_sock.recvfrom(65536)
        if self.debug_print:
            print '[mmRemote::runCommand] received result!...'
        rcvList = array.array('B', data)
        resultBuf = mmapi.vectorub(rcvList)
        serializer.setBuffer(resultBuf)
        cmd.Restore_Results(serializer)