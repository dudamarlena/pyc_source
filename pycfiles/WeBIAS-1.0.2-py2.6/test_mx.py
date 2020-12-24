# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/webias/gnosis/xml/pickle/test/test_mx.py
# Compiled at: 2015-04-13 16:10:48
"""Test mxDateTime pickling --fpm"""
import mx.DateTime as date, UserList, UserDict
from types import *
import gnosis.xml.pickle as xml_pickle
from gnosis.xml.pickle.util import setParanoia
import funcs
funcs.set_parser()

class foo_class:

    def __init__(self):
        pass


def testfoo(o1, o2):
    for attr in ['t', 'd', 'ud', 'l', 'ul', 'tup']:
        if getattr(o1, attr) != getattr(o2, attr):
            raise 'ERROR(1)'


def printfoo(obj):
    print type(obj.t), obj.t
    print type(obj.d), obj.d['One'], obj.d['Two']
    print type(obj.ud), obj.ud['One'], obj.ud['Two']
    print type(obj.l), obj.l[0], obj.l[1]
    print type(obj.ul), obj.ul[0], obj.ul[1]
    print type(obj.tup), obj.tup[0], obj.tup[1]


foo = foo_class()
setParanoia(0)
foo.t = date.DateTime(2000, 1, 2, 3, 4, 5.6)
foo.d = {'One': date.DateTime(2001, 2, 3, 4, 5, 6.7), 'Two': date.DateTime(2002, 3, 4, 5, 6, 7.8)}
foo.ud = UserDict.UserDict()
foo.ud['One'] = date.DateTime(2003, 4, 5, 6, 7, 8.9)
foo.ud['Two'] = date.DateTime(2004, 5, 6, 7, 8, 9.1)
foo.l = []
foo.l.append(date.DateTime(2005, 6, 7, 8, 9, 10.11))
foo.l.append(date.DateTime(2006, 7, 8, 9, 10, 11.12))
foo.ul = UserList.UserList()
foo.ul.append(date.DateTime(2007, 8, 9, 10, 11, 12.13))
foo.ul.append(date.DateTime(2008, 9, 10, 11, 12, 13.14))
foo.tup = (
 date.DateTime(2009, 10, 11, 12, 13, 14.15),
 date.DateTime(2010, 11, 12, 13, 14, 15.16))
x1 = xml_pickle.dumps(foo)
bar = xml_pickle.loads(x1)
testfoo(foo, bar)
x2 = xml_pickle.dumps(bar)
print '** OK **'