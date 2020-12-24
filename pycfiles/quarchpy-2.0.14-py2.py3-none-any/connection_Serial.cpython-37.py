# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\sboon\AppData\Local\Temp\pip-install-ptdbtr91\quarchpy\quarchpy\connection_specific\connection_Serial.py
# Compiled at: 2020-03-25 05:10:07
# Size of source mod 2**32: 1834 bytes
import datetime, serial, time
import serial.tools.list_ports as serialList

def serial_read_until(Port, Char, Timeout):
    ReturnStr = b''
    Start = datetime.datetime.now()
    Done = False
    while Done == False:
        while Port.inWaiting() > 0:
            NewChar = Port.read(1)
            if NewChar == Char:
                return ReturnStr
            ReturnStr += NewChar
            Start = datetime.datetime.now()

        Now = datetime.datetime.now()
        if (Now - Start).seconds > Timeout:
            return ReturnStr

    return ReturnStr


class SerialConn:

    def __init__(self, ConnTarget):
        self.ConnTarget = ConnTarget
        self.Connection = serial.Serial(port=(self.ConnTarget), baudrate=19200,
          parity=(serial.PARITY_NONE),
          stopbits=(serial.STOPBITS_ONE),
          bytesize=(serial.EIGHTBITS))

    def close(self):
        self.Connection.close()
        return True

    def sendCommand(self, Command, expectedResponse=True):
        Command = (Command + '\r\n').encode()
        self.Connection.write(Command)
        Result = serial_read_until(self.Connection, b'\n', 3)
        Result = serial_read_until(self.Connection, b'>', 3).strip()
        Result = Result.decode()
        Result = Result.strip('> \t\n\r')
        return Result.strip()