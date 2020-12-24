# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/webias/gnosis/xml/pickle/test/test_re.py
# Compiled at: 2015-04-13 16:10:48
"""Demonstrate that SRE xml pickling works --fpm """
import UserList, UserDict, sys
from types import *
import gnosis.xml.pickle as xml_pickle, re, StringIO
from gnosis.xml.pickle.util import setParanoia, getParanoia
import funcs
funcs.set_parser()

class foo_class:

    def __init__(self):
        pass


def checkfoo(o1, o2):
    if o1.__class__ != foo_class or o2.__class__ != foo_class:
        raise 'ERROR(0)'
    for attr in ['sre', 'd', 'ud', 'l', 'ul', 'tup']:
        if getattr(o1, attr) != getattr(o2, attr):
            raise 'ERROR(1)'


def printfoo(obj):
    print type(obj.sre), obj.sre.pattern
    print type(obj.d),
    print ':%s:%s:' % (obj.d['One'].pattern, obj.d['Two'].pattern)
    print type(obj.ud),
    print ':%s:%s:' % (obj.ud['OneOne'].pattern, obj.ud['TwoTwo'].pattern)
    print type(obj.l),
    print ':%s:%s' % (obj.l[0].pattern, obj.l[1].pattern)
    print type(obj.ul),
    print ':%s:%s' % (obj.ul[0].pattern, obj.ul[1].pattern)
    print type(obj.tup),
    print ':%s:%s:' % (obj.tup[0].pattern, obj.tup[1].pattern)


foo = foo_class()
setParanoia(0)
foo.sre = re.compile('\\S+\\s+\\S+sss')
foo.d = {'One': re.compile('[abc]+<escape me>\n[1-9]*'), 'Two': re.compile('\\s+1234[a-z]+$')}
foo.ud = UserDict.UserDict()
foo.ud['OneOne'] = re.compile('^He[l]+o\\s+')
foo.ud['TwoTwo'] = re.compile('world$')
foo.l = []
foo.l.append(re.compile('[foo|bar]?'))
foo.l.append(re.compile('[qrs]+[1-9]?'))
foo.ul = UserList.UserList()
foo.ul.append(re.compile('[+\\-][0-9]+'))
foo.ul.append(re.compile('(bored yet)?'))
foo.tup = (
 re.compile('this is [not]? '), re.compile('a [tuple|list]'))
x1 = xml_pickle.dumps(foo)
bar = xml_pickle.loads(x1)
checkfoo(foo, bar)
x2 = xml_pickle.dumps(bar)
baz = xml_pickle.loads(x2)
checkfoo(bar, baz)
print '** OK **'