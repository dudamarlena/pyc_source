# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/webias/gnosis/xml/pickle/test/test_subbltin.py
# Compiled at: 2015-04-13 16:10:48
"""Test pickling of objects that are subclassed from builtins       --fpm"""
import gnosis.xml.pickle as xml_pickle, funcs
funcs.set_parser()

class top:
    pass


class lcombo(list):

    def __init__(self, initlist, a, b):
        list.__init__(self, initlist)
        self.a = a
        self.b = b


class dcombo(dict):

    def __init__(self, initdict, a, b):
        dict.__init__(self, initdict)
        self.a = a
        self.b = b


class _tcombo(tuple):

    def __init__(self, inittup):
        tuple.__init__(self, inittup)


def tcombo(inittup, a, b):
    t = _tcombo(inittup)
    t.a = a
    t.b = b
    return t


class _icombo(int):

    def __init__(self, initi):
        int.__init__(self, initi)


def icombo(initi, a, b):
    i = _fcombo(initi)
    i.a = a
    i.b = b
    return i


class _fcombo(float):

    def __init__(self, initf):
        float.__init__(self, initf)


def fcombo(initf, a, b):
    f = _fcombo(initf)
    f.a = a
    f.b = b
    return f


class _ccombo(complex):

    def __init__(self, initc):
        complex.__init__(self, initc)


def ccombo(initc, a, b):
    c = _ccombo(initc)
    c.a = a
    c.b = b
    return c


class _scombo(str):

    def __init__(self, inits):
        str.__init__(self, inits)


def scombo(inits, a, b):
    s = _scombo(inits)
    s.a = a
    s.b = b
    return s


class _ucombo(unicode):

    def __init__(self, initu):
        unicode.__init__(self, initu)


def ucombo(initu, a, b):
    s = _ucombo(initu)
    s.a = a
    s.b = b
    return s


class lcore(list):
    pass


class dcore(dict):
    pass


class tcore(tuple):
    pass


class icore(int):
    pass


class locore(long):
    pass


class fcore(float):
    pass


class ccore(complex):
    pass


class score(str):
    pass


class ucore(unicode):
    pass


xml_pickle.setParanoia(0)

def check_combo(o1, o2):
    if o1.__class__ != o2.__class__ or o1.a != o2.a or o1.a.a != o2.a.a or o1.a.b != o2.a.b or o1.a.zz != o2.a.zz:
        raise 'ERROR(1)'


x = top()
x.a = lcombo([4, 5, 6], 1, 2)
x.a.zz = 10
s = xml_pickle.dumps(x)
g = xml_pickle.loads(s)
check_combo(x, g)
x = top()
x.a = dcombo({'a': 1, 'b': 2, 'c': 3}, 1, 2)
x.a.zz = 10
s = xml_pickle.dumps(x)
g = xml_pickle.loads(s)
check_combo(x, g)
x = top()
x.a = tcombo((10, 11, 12), 1, 2)
x.a.zz = 10
s = xml_pickle.dumps(x)
g = xml_pickle.loads(s)
check_combo(x, g)
x = top()
x.a = fcombo(321, 1, 2)
x.a.zz = 10
s = xml_pickle.dumps(x)
g = xml_pickle.loads(s)
check_combo(x, g)
x = top()
x.a = fcombo(5.23, 1, 2)
x.a.zz = 10
s = xml_pickle.dumps(x)
g = xml_pickle.loads(s)
check_combo(x, g)
x = top()
x.a = ccombo(complex(234.0, 567.0), 1, 2)
x.a.zz = 10
s = xml_pickle.dumps(x)
g = xml_pickle.loads(s)
check_combo(x, g)
x = top()
x.a = scombo('a string combo', 1, 2)
x.a.zz = 10
s = xml_pickle.dumps(x)
g = xml_pickle.loads(s)
check_combo(x, g)
x = top()
x.a = ucombo('a unicode combo', 1, 2)
x.a.zz = 10
s = xml_pickle.dumps(x)
g = xml_pickle.loads(s)
check_combo(x, g)

def check_core(o1, o2):
    if o1.__class__ != o2.__class__ or o1.a != o2.a:
        raise 'ERROR(2)'


x = top()
x.a = lcore([10, 11, 12])
s = xml_pickle.dumps(x)
g = xml_pickle.loads(s)
check_core(x, g)
x = top()
x.a = dcore({'a': 1, 'b': 2, 'c': 3})
s = xml_pickle.dumps(x)
g = xml_pickle.loads(s)
check_core(x, g)
x = top()
x.a = tcore((10, 11, 12))
s = xml_pickle.dumps(x)
g = xml_pickle.loads(s)
check_core(x, g)
x = top()
x.a = icore(145)
s = xml_pickle.dumps(x)
g = xml_pickle.loads(s)
check_core(x, g)
x = top()
x.a = icore(12345)
s = xml_pickle.dumps(x)
g = xml_pickle.loads(s)
check_core(x, g)
x = top()
x.a = fcore(123.45)
s = xml_pickle.dumps(x)
g = xml_pickle.loads(s)
check_core(x, g)
x = top()
x.a = ccore(complex(123.0, 456.0))
s = xml_pickle.dumps(x)
g = xml_pickle.loads(s)
check_core(x, g)
x = top()
x.a = score('hello score')
s = xml_pickle.dumps(x)
g = xml_pickle.loads(s)
check_core(x, g)
x = top()
x.a = ucore('hello ucore')
s = xml_pickle.dumps(x)
g = xml_pickle.loads(s)
check_core(x, g)
x = lcombo([6, 7, 8], 1, 2)
s = xml_pickle.dumps(x)
g = xml_pickle.loads(s)
if g.a != x.a or g.b != x.b:
    raise 'ERROR(3)'
x = lcore([6, 7, 8])
s = xml_pickle.dumps(x)
g = xml_pickle.loads(s)
if x != g:
    raise 'ERROR(4)'
x = lcore()
s = xml_pickle.dumps(x)
g = xml_pickle.loads(s)
if x != g:
    raise 'ERROR(5)'
x = dcore()
s = xml_pickle.dumps(x)
g = xml_pickle.loads(s)
if x != g:
    raise 'ERROR(6)'
x = tcore()
s = xml_pickle.dumps(x)
g = xml_pickle.loads(s)
if x != g:
    raise 'ERROR(7)'
print '** OK **'