# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/webias/gnosis/xml/pickle/test/test_bltin.py
# Compiled at: 2015-04-13 16:10:47
from types import *
import gnosis.xml.pickle as xml_pickle
from gnosis.xml.pickle.util import setInBody
import funcs
funcs.set_parser()

class foo_class:

    def __init__(self):
        pass


def checkfoo(o1, o2):
    """Check that objects match (sync w/obj creation below)"""
    if o1.__class__ != foo_class or o2.__class__ != foo_class:
        raise 'ERROR(0)'
    for attr in ['s1', 's2', 'f', 'i', 'i2', 'li',
     'j', 'n', 'd', 'l', 'tup']:
        if getattr(o1, attr) != getattr(o2, attr):
            raise 'ERROR(1)'


xml_pickle.setParanoia(0)
foo = foo_class()
setInBody(ComplexType, 1)
foo.s1 = 'this is a " string with a \' in it'
foo.s2 = 'this is a \' string with a " in it'
foo.f = 123.456
foo.i = 789
foo.i2 = 0
foo.li = 5678
foo.j = complex(12.0, 34.0)
foo.n = None
foo.d = {'One': 'First dict item', 'Two': 222, 
   'Three': 333.444}
foo.l = []
foo.l.append('first list')
foo.l.append(321)
foo.l.append(12.34)
foo.tup = ('tuple', 123, 444.333)
x1 = xml_pickle.XML_Pickler(foo).dumps()
bar = xml_pickle.XML_Pickler().loads(x1)
checkfoo(foo, bar)
print '** OK **'