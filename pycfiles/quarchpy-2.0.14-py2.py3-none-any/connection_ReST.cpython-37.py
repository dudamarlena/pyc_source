# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\sboon\AppData\Local\Temp\pip-install-ptdbtr91\quarchpy\quarchpy\connection_specific\connection_ReST.py
# Compiled at: 2020-03-25 05:10:07
# Size of source mod 2**32: 1063 bytes
try:
    import httplib
except ImportError:
    import http.client as httplib

class ReSTConn:

    def __init__(self, ConnTarget):
        self.ConnTarget = ConnTarget
        self.Connection = httplib.HTTPConnection((self.ConnTarget), 80, timeout=10)
        self.Connection.close()

    def close(self):
        return True

    def sendCommand(self, Command, expectedResponse=True):
        Command = '/' + Command.replace(' ', '%20')
        self.Connection.request('GET', Command)
        if expectedResponse == True:
            R2 = self.Connection.getresponse()
            if R2.status == 200:
                Result = R2.read()
                Result = Result.decode()
                Result = Result.strip('> \t\n\r')
                self.Connection.close()
                return Result
            print('FAIL - Please power cycle the module!')
            self.Connection.close()
            return ('FAIL: ', R1.status, R1.reason)
        else:
            return