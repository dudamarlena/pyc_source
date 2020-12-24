# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.4-x86_64/egg/gunicorn_thrift/thrift/protocol.py
# Compiled at: 2014-09-15 23:09:53
import sys
from thrift.protocol.TBinaryProtocol import TBinaryProtocol

class TBinaryProtocolExt(TBinaryProtocol):
    """encode unicode to utf8 in python2.x,before send.
    """

    def writeString(self, msg):
        if sys.version_info[0] >= 3 and not isinstance(msg, bytes):
            msg = msg.encode('utf-8')
        elif sys.version_info[0] == 2 and isinstance(msg, unicode):
            msg = msg.encode('utf8')
        self.writeI32(len(msg))
        self.trans.write(msg)

    def readString(self):
        len = self.readI32()
        s = self.trans.readAll(len)
        if sys.version_info[0] == 2 and isinstance(s, str):
            s = unicode(s, 'utf8')
        return s


class TBinaryProtocolFactoryExt(object):

    def __init__(self, strictRead=False, strictWrite=True):
        self.strictRead = strictRead
        self.strictWrite = strictWrite

    def getProtocol(self, trans):
        prot = TBinaryProtocolExt(trans, self.strictRead, self.strictWrite)
        return prot