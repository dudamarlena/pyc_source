# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/webias/gnosis/xml/pickle/test/test_getinitargs.py
# Compiled at: 2015-04-13 16:10:48
"""
test that we get the tricky stuff correct between
__getstate__ and __getinitargs__ --fpm
"""
import pickle, gnosis.xml.pickle as xml_pickle, funcs
from copy import copy
from UserList import UserList
funcs.set_parser()
xml_pickle.setParanoia(0)
COUNT_INIT = 0
COUNT_GETARGS = 0

class Foo:
    __safe_for_unpickling__ = 1

    def __init__(self, a, b, c, d):
        global COUNT_INIT
        COUNT_INIT += 1
        if len(self.__dict__.keys()) != 0:
            raise "ERROR -- attrs shouldn't exist before __init__"
        self.a = a
        self.b = b
        self.c = c
        self.d = d

    def __getinitargs__(self):
        global COUNT_GETARGS
        COUNT_GETARGS += 1
        return (
         200, 'def', [4, 5, 6], ('x', 'y', 'z'))

    def __getstate__(self):
        d = copy(self.__dict__)
        del d['c']
        del d['d']
        return d


def check_foo(o1, o2, NR):
    if o1.__class__ != Foo or o2.__class__ != Foo or o1.a != o2.a or o1.b != o2.b or o2.c != o1.__getinitargs__()[2] or o2.d != o1.__getinitargs__()[3]:
        raise 'ERROR(%d)' % NR


x = Foo(1, 'abc', [1, 2, 3], ('a', 'b', 'c'))
p = pickle.dumps(x)
x2 = pickle.loads(p)
check_foo(x, x2, 1)
px = xml_pickle.dumps(x)
x3 = xml_pickle.loads(px)
check_foo(x, x3, 2)
if COUNT_INIT != 3 or COUNT_GETARGS != 6:
    raise 'ERROR(3)'
f = Foo(1, 2, 3, 4)
f.x = Foo(5, 6, 7, 8)
f.y = UserList(['x', 'y', 'z'])
f.y += [Foo(9, 10, 11, 12), UserList(['a', 'b', 'c'])]
f.z = [
 1, 2, 3, UserList([4, 5, Foo(13, 14, 15, 16)])]
x = xml_pickle.dumps(f)
o = xml_pickle.loads(x)
check_foo(f, o, 4)
check_foo(f.x, o.x, 5)
check_foo(f.y[3], o.y[3], 5)
check_foo(f.z[3][2], o.z[3][2], 6)
print '** OK **'