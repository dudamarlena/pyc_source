# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/quebert/phelpers.py
# Compiled at: 2009-09-03 15:03:57
import sys
from twisted.protocols import basic
from twisted.python import reflect

class FakeTransport(object):

    def __init__(self, in_, out):
        self.in_ = in_
        self.out = out

    def loseConnection(self):
        self.in_.close()
        self.out.close()

    def write(self, data):
        self.out.write(data)

    def read(self, bytes):
        return self.in_.read(bytes)


class FakeProtocol(basic.Int32StringReceiver):
    MAX_LENGTH = 16777216

    def __init__(self, entrypoint, *args):
        self.entrypoint = entrypoint
        self.args = args

    def stringReceived(self, data):
        result = self.entrypoint(data, *self.args)
        self.sendString(str(result))


def parseTask(entrypoint, args=None, input=sys.stdin, output=sys.stdout):
    t = FakeTransport(input, output)
    protocol = FakeProtocol(entrypoint, *args)
    protocol.makeConnection(t)
    while True:
        in_ = t.read(1024)
        if not in_:
            break
        protocol.dataReceived(in_)


def main():
    entryp = sys.argv[1]
    args = sys.argv[2:]
    entry = reflect.namedAny(entryp)
    parseTask(entry, args)