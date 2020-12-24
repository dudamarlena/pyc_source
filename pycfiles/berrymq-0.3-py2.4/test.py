# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/tests/test.py
# Compiled at: 2009-07-29 04:01:24
from client import *
from server import *

def test():
    if not len(sys.argv) > 1:
        import socket
        print 'Running JSON-RPC server on port 8000'
        server = SimpleJSONRPCServer(('localhost', 8000))
        server.register_function(pow)
        server.register_function(lambda x, y: x + y, 'add')
        server.serve_forever()
    else:
        remote = ServerProxy(sys.argv[1])
        print 'Using connection', remote
        print repr(remote.add(1, 2))
        aaa = remote.add
        print repr(remote.pow(2, 4))
        print aaa(5, 6)
        try:
            aaa(5, 'toto')
            print 'Successful execution of invalid code'
        except Fault:
            pass

        try:
            aaa(5, 6, 7)
            print 'Successful execution of invalid code'
        except Fault:
            pass

        try:
            print repr(remote.powx(2, 4))
            print 'Successful execution of invalid code'
        except Fault:
            pass


if __name__ == '__main__':
    test()