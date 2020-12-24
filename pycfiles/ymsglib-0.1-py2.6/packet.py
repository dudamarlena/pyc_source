# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\ymsg\packet.py
# Compiled at: 2009-11-08 13:05:04


class BadHeader(Exception):
    pass


class Packet:

    def __init__(self):
        self.type = ''
        self.dsep = b'\xc0\x80'
        self.magic = 'YMSG'
        self.version = '\x00\x10\x00\x00'
        self.length = ''
        self.service = ''
        self.status = ''
        self.sid = ''
        self.body = ''

    def __getitem__(self, key):
        body = self.getBody()
        if key in body:
            try:
                return body[(body.index(str(key)) + 1)]
            except:
                return

        return

    def packInt16(self, n):
        return self.packInt(n, 2)

    def packInt32(self, n):
        return self.packInt(n, 4)

    def packInt(self, n, size):
        s = ''
        for i in xrange(size):
            s = chr(n & 255) + s
            n >>= 8

        return s

    def unpackInt(self, s):
        c = 0
        for i in s:
            c <<= 8
            c += ord(i)

        return c

    def packData(self, data):
        return self.dsep.join(data) + self.dsep

    def unpackData(self, data):
        return data.split(self.dsep)

    def setType(self, s):
        self.type = s

    def setService(self, d):
        self.service = self.packInt16(d)

    def setStatus(self, d):
        self.status = self.packInt32(d)

    def setSid(self, d):
        self.sid = self.packInt32(d)

    def appendBody(self, l):
        self.body += self.packData(l)
        self.length = self.packInt16(len(self.body))

    def getLength(self):
        return self.unpackInt(self.length)

    def getService(self):
        return self.unpackInt(self.service)

    def getStatus(self):
        return self.unpackInt(self.status)

    def getSid(self):
        return self.unpackInt(self.sid)

    def getBody(self):
        return self.unpackData(self.body)

    def getPacketData(self):
        if self.length == '':
            self.length = self.packInt16(len(self.body))
        return '%s%s%s%s%s%s%s' % (self.magic, self.version, self.length,
         self.service, self.status, self.sid, self.body)

    def __repr__(self):
        return '<Packet Type=%s, Ymsg=%s, Version=0x%x, Length=%d, Service=0x%x, Status=0x%x, Sid=%d, Body=%r>' % (
         self.type,
         self.magic, ord(self.version[1]), self.getLength(),
         self.getService(), self.getStatus(), self.getSid(), self.getBody())