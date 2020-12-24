# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/ant/core/log.py
# Compiled at: 2011-10-07 13:51:09
import time, datetime, msgpack
EVENT_OPEN = 1
EVENT_CLOSE = 2
EVENT_READ = 3
EVENT_WRITE = 4

class LogReader(object):

    def __init__(self, filename):
        self.is_open = False
        self.open(filename)

    def __del__(self):
        if self.is_open:
            self.fd.close()

    def open(self, filename):
        if self.is_open == True:
            self.close()
        self.fd = open(filename, 'r')
        self.is_open = True
        self.unpacker = msgpack.Unpacker()
        self.unpacker.feed(self.fd.read())
        self.fd.close()
        header = self.unpacker.unpack()
        if len(header) != 2 or header[0] != 'ANT-LOG' or header[1] != 1:
            raise IOError('Could not open log file (unknown format).')

    def close(self):
        if self.is_open:
            self.fd.close()
            self.is_open = False

    def read(self):
        try:
            return self.unpacker.unpack()
        except StopIteration:
            return

        return


class LogWriter(object):

    def __init__(self, filename=''):
        self.packer = msgpack.Packer()
        self.is_open = False
        self.open(filename)

    def __del__(self):
        if self.is_open:
            self.fd.close()

    def open(self, filename=''):
        if filename == '':
            filename = datetime.datetime.now().isoformat() + '.ant'
        self.filename = filename
        if self.is_open == True:
            self.close()
        self.fd = open(filename, 'w')
        self.is_open = True
        self.packer = msgpack.Packer()
        header = [
         'ANT-LOG', 1]
        self.fd.write(self.packer.pack(header))

    def close(self):
        if self.is_open:
            self.fd.close()
            self.is_open = False

    def _logEvent(self, event, data=None):
        ev = [event, int(time.time()), data]
        if data is None:
            ev = ev[0:-1]
        elif len(data) == 0:
            return
        self.fd.write(self.packer.pack(ev))
        return

    def logOpen(self):
        self._logEvent(EVENT_OPEN)

    def logClose(self):
        self._logEvent(EVENT_CLOSE)

    def logRead(self, data):
        self._logEvent(EVENT_READ, data)

    def logWrite(self, data):
        self._logEvent(EVENT_WRITE, data)