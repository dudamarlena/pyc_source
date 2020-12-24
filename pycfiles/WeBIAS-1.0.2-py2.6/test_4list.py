# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/webias/gnosis/xml/pickle/test/test_4list.py
# Compiled at: 2015-04-13 16:10:47
"""exercise all 4 list-writing methods --fpm"""
import gnosis.xml.pickle as xml_pickle, sys, funcs
funcs.set_parser()

class foo:
    pass


f = foo()
f.a = (1, 2, 3)
x = xml_pickle.dumps(f)
if x[0:5] == '<?xml':
    print 'OK'
else:
    print 'ERROR'
    sys.exit(1)
g = xml_pickle.loads(x)
if g.a == (1, 2, 3):
    print 'OK'
else:
    print 'ERROR'
    sys.exit(1)
x = xml_pickle.dumps(f, 1)
if x[0:2] == b'\x1f\x8b':
    print 'OK'
else:
    print 'ERROR'
    sys.exit(1)
g = xml_pickle.loads(x)
if g.a == (1, 2, 3):
    print 'OK'
else:
    print 'ERROR'
    sys.exit(1)
fh = open('aaa', 'wb')
xml_pickle.dump(f, fh)
fh.close()
fh = open('aaa', 'rb')
line = fh.read(5)
if line == '<?xml':
    print 'OK'
else:
    print 'ERROR'
    sys.exit(1)
fh.close()
fh = open('aaa', 'rb')
g = xml_pickle.load(fh)
if g.a == (1, 2, 3):
    print 'OK'
else:
    print 'ERROR'
    sys.exit(1)
fh.close()
fh = open('aaa', 'wb')
xml_pickle.dump(f, fh, 1)
fh.close()
fh = open('aaa', 'rb')
line = fh.read(2)
if line == b'\x1f\x8b':
    print 'OK'
else:
    print 'ERROR'
    sys.exit(1)
fh.close()
fh = open('aaa', 'rb')
g = xml_pickle.load(fh)
if g.a == (1, 2, 3):
    print 'OK'
else:
    print 'ERROR'
    sys.exit(1)
fh.close()
funcs.unlink('aaa')