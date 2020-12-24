# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\sboon\AppData\Local\Temp\pip-install-ptdbtr91\quarchpy\quarchpy\connection.py
# Compiled at: 2020-03-25 05:10:07
# Size of source mod 2**32: 2240 bytes
import quarchpy.connection_specific.connection_QPS as qpsInterface
import quarchpy.connection_specific.connection_QIS as qisInterface

class QISConnection:

    def __init__(self, ConString, host, port):
        self.qis = qisInterface(host, port)


class PYConnection:

    def __init__(self, ConString):
        Pos = ConString.find(':')
        if Pos == -1:
            raise ValueError('Please check your module name!')
        else:
            self.ConnTypeStr = ConString[0:Pos].upper()
            self.ConnTarget = ConString[Pos + 1:]
            if 'SERIAL' not in self.ConnTypeStr:
                self.ConnTarget = ConString[Pos + 1:].upper()
            elif self.ConnTypeStr.lower() == 'rest':
                from quarchpy.connection_specific.connection_ReST import ReSTConn
                if 'qtl' in self.ConnTarget.lower():
                    self.ConnTarget.replace('qtl', '')
                self.connection = ReSTConn(self.ConnTarget)
            else:
                if self.ConnTypeStr.lower() == 'usb':
                    from quarchpy.connection_specific.connection_USB import USBConn
                    self.connection = USBConn(self.ConnTarget)
                else:
                    if self.ConnTypeStr.lower() == 'serial':
                        from quarchpy.connection_specific.connection_Serial import SerialConn
                        self.connection = SerialConn(self.ConnTarget)
                    else:
                        if self.ConnTypeStr.lower() == 'telnet':
                            from quarchpy.connection_specific.connection_Telnet import TelnetConn
                            self.connection = TelnetConn(self.ConnTarget)
                        else:
                            if self.ConnTypeStr.lower() == 'tcp':
                                from quarchpy.connection_specific.connection_TCP import TCPConn
                                self.connection = TCPConn(self.ConnTarget)
                            else:
                                raise ValueError('Invalid connection type in module string!')


class QPSConnection:

    def __init__(self, host, port):
        self.qps = qpsInterface(host, port)