# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/atron_cli/board.py
# Compiled at: 2019-03-27 01:45:18
import serial, time, ampy
from ampy.pyboard import PyboardError
from ampy.files import PyboardError as FilesError
from ampy.files import DirectoryExistsError
COMMAND_CTRL_A = '\r\x01'
COMMAND_CTRL_B = '\r\x02'
COMMAND_CTRL_C = '\r\x03'
COMMAND_CTRL_D = '\r\x04'

class BoardException(BaseException):
    pass


class Board:

    def __init__(self, device, baudrate=115200):
        try:
            self.board = ampy.pyboard.Pyboard(device=device, baudrate=baudrate)
            self.files = ampy.files.Files(self.board)
        except (PyboardError, OSError, IOError):
            raise BoardException('failed to access ' + device)
        except FilesError:
            raise BoardException('failed to access files on ' + device)

    def close(self):
        self.board.close()

    def soft_reset(self):
        serial = self.board.serial
        serial.write(COMMAND_CTRL_C)
        time.sleep(0.1)
        serial.write(COMMAND_CTRL_C)
        n = serial.inWaiting()
        while n > 0:
            serial.read(n)
            n = serial.inWaiting()

        time.sleep(0.1)
        serial.write(COMMAND_CTRL_D)
        data = self.board.read_until(1, 'soft reboot\r\n')
        if not data.endswith('soft reboot\r\n'):
            raise BoardException('could not soft_reset')