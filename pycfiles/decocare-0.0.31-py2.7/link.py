# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/decocare/link.py
# Compiled at: 2016-03-06 17:04:33
import serial, logging, lib, fuser
io = logging.getLogger()
log = io.getChild(__name__)

class AlreadyInUseException(Exception):
    pass


class Link(object):
    __timeout__ = 0.5
    port = None

    def __init__(self, port, timeout=None):
        if timeout is not None:
            self.__timeout__ = timeout
        if fuser.in_use(port):
            raise AlreadyInUseException(('{port} already in use').format(port=port))
        self.open(port, dsrdtr=True, rtscts=True)
        return

    def open(self, newPort=False, **kwds):
        if newPort:
            self.port = newPort
        if 'timeout' not in kwds:
            kwds['timeout'] = self.__timeout__
        kwds['rtscts'] = True
        kwds['dsrdtr'] = True
        self.serial = serial.Serial(self.port, **kwds)
        if self.serial.isOpen():
            log.info(('{agent} opened serial port: {serial}').format(serial=repr(self.serial), agent=self.__class__.__name__))

    def close(self):
        io.info('closing serial port')
        return self.serial.close()

    def write(self, string):
        r = self.serial.write(string)
        io.info('usb.write.len: %s\n%s' % (len(string),
         lib.hexdump(bytearray(string))))
        return r

    def read(self, c):
        r = self.serial.read(c)
        io.info('usb.read.len: %s' % len(r))
        io.info('usb.read.raw:\n%s' % lib.hexdump(bytearray(r)))
        return r

    def readline(self):
        r = self.serial.readline()
        io.info('usb.read.len: %s\n%s' % (len(r),
         lib.hexdump(bytearray(r))))
        return r

    def readlines(self):
        r = self.serial.readlines()
        io.info('usb.read.len: %s\n%s' % (len(r),
         lib.hexdump(bytearray(('').join(r)))))
        return r


if __name__ == '__main__':
    import doctest
    doctest.testmost()