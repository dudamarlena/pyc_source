# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\sboon\AppData\Local\Temp\pip-install-ptdbtr91\quarchpy\quarchpy\connection_specific\connection_Telnet.py
# Compiled at: 2020-03-25 05:10:07
# Size of source mod 2**32: 676 bytes
import telnetlib, time

class TelnetConn:

    def __init__(self, ConnTarget):
        self.ConnTarget = ConnTarget
        self.Connection = telnetlib.Telnet(self.ConnTarget)
        time.sleep(1)
        self.Connection.read_very_eager()

    def close(self):
        self.Connection.close()
        return True

    def sendCommand(self, Command, expectedResponse=True):
        self.Connection.write((Command + '\r\n').encode('latin-1'))
        self.Connection.read_until(b'\r\n', 3)
        Result = self.Connection.read_until(b'>', 3)[:-1]
        Result = Result.decode()
        Result = Result.strip('> \t\n\r')
        return Result.strip()