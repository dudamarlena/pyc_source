# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/webias/gnosis/xml/pickle/test/test_bools.py
# Compiled at: 2015-04-13 16:10:47
import gnosis.xml.pickle as xmp
from gnosis.xml.pickle.util import setVerbose, setParanoia
from funcs import set_parser, unlink
from types import *
SHOW_XML = 0
set_parser()

class a_test_class:

    def __init__(self):
        pass


def a_test_function():
    pass


class foo:

    def __init__(self):
        self.a = False
        self.b = True
        self.c = None
        self.f = a_test_function
        self.k = a_test_class
        return


setVerbose(1)
setParanoia(0)
f = foo()
s = xmp.dumps(f)
if SHOW_XML:
    print s
x = xmp.loads(s)
for attr in ['a', 'b', 'c', 'f', 'k']:
    if getattr(f, attr) != getattr(x, attr):
        raise 'ERROR(1)'

s = xmp.dumps((True, False))
if SHOW_XML:
    print s
x = xmp.loads(s)
if x[0] != True or x[1] != False:
    raise 'ERROR(2)'
s = xmp.dumps(True)
if SHOW_XML:
    print s
x = xmp.loads(s)
if x != True:
    raise 'ERROR(3)'
print '** OK **'