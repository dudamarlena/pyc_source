# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/PIL/ContainerIO.py
# Compiled at: 2007-09-25 20:00:35


class ContainerIO:

    def __init__(self, file, offset, length):
        self.fh = file
        self.pos = 0
        self.offset = offset
        self.length = length
        self.fh.seek(offset)

    def isatty(self):
        return 0

    def seek(self, offset, mode=0):
        if mode == 1:
            self.pos = self.pos + offset
        elif mode == 2:
            self.pos = self.length + offset
        else:
            self.pos = offset
        self.pos = max(0, min(self.pos, self.length))
        self.fh.seek(self.offset + self.pos)

    def tell(self):
        return self.pos

    def read(self, n=0):
        if n:
            n = min(n, self.length - self.pos)
        else:
            n = self.length - self.pos
        if not n:
            return ''
        self.pos = self.pos + n
        return self.fh.read(n)

    def readline(self):
        s = ''
        while 1:
            c = self.read(1)
            if not c:
                break
            s = s + c
            if c == '\n':
                break

        return s

    def readlines(self):
        l = []
        while 1:
            s = self.readline()
            if not s:
                break
            l.append(s)

        return l