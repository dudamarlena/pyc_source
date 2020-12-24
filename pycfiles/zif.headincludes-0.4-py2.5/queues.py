# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/zif/headincludes/queues.py
# Compiled at: 2010-03-12 11:12:03
"""
useful queues for wsgi middleware
"""
import tempfile

class TemporaryFileQueue(object):

    def __init__(self):
        self.file = tempfile.TemporaryFile()
        self.readPointer = 0
        self.writePointer = 0

    def read(self, bytes=None):
        self.file.flush()
        self.file.seek(self.readPointer)
        if bytes:
            s = self.file.read(bytes)
        else:
            s = self.file.read()
        self.readPointer = self.file.tell()
        return s

    def write(self, data):
        self.file.seek(self.writePointer)
        self.file.write(data)
        self.writePointer = self.file.tell()

    def __len__(self):
        return self.writePointer - self.readPointer

    def close(self):
        self.file.close()
        self.file = None
        return


class StringQueue(object):

    def __init__(self, data=''):
        self.l_buffer = []
        self.s_buffer = ''
        self.write(data)

    def write(self, data):
        if not isinstance(data, basestring):
            raise TypeError, 'argument 1 must be string, not %s' % type(data).__name__
        self.l_buffer.append(data)

    def _build_str(self):
        new_string = ('').join(self.l_buffer)
        self.s_buffer = ('').join((self.s_buffer, new_string))
        self.l_buffer = []

    def __len__(self):
        return sum((len(i) for i in self.l_buffer)) + len(self.s_buffer)

    def close(self):
        self.__init__()

    def read(self, count=None):
        if count > len(self.s_buffer) or count == None:
            self._build_str()
        if count > len(self.s_buffer):
            return ''
        result = self.s_buffer[:count]
        self.s_buffer = self.s_buffer[len(result):]
        return result