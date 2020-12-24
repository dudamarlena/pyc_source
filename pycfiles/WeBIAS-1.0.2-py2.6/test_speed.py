# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/webias/gnosis/xml/pickle/test/test_speed.py
# Compiled at: 2015-04-13 16:10:48
"""Test harness for measuring the speed of different parsers. --fpm"""
import gnosis.xml.pickle as xml_pickle
from xml.dom import minidom
from UserList import UserList
from UserDict import UserDict
import re, os
from stat import *
from time import time

class foo:
    pass


def mk_foo(level=5):
    f = foo()
    l = [
     1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    t = (1.2, 2.3, 3.4, 4.5, 5.6, 6.7, 7.8, 8.9, 9.1, 10.2)
    d = {'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6, 'seven': 7, 'eight': 8, 
       'nine': 9, 'ten': 10}
    c = [complex(1.0, 2.0), complex(2.0, 3.0), complex(3.0, 4.0), complex(4.0, 5.0), complex(5.0, 6.0), complex(6.0, 7.0), complex(7.0, 8.0), complex(8.0, 9.0), complex(9.0, 10.0), complex(10.0, 11.0)]
    s = ('one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten')
    ll = [
     l, l, l, l, l,
     t, t, t, t, t,
     d, d, d, d, d,
     c, c, c, c, c,
     s, s, s, s, s]
    u = [
     ll, ll, ll, ll, ll, ll, ll, ll]
    f.u = [
     u, u, u, u, u, u, u, u]
    if level >= 5:
        f.uu = [f.u, f.u, f.u, f.u, f.u, f.u]
    if level >= 6:
        f.uuu = [f.uu, f.uu, f.uu, f.uu, f.uu, f.uu]
    return f


def doit3():

    class foo:
        pass

    f = foo()
    f.a = 1
    f.b = f.a
    f.c = 'abc'
    f.d = f.c
    f.r = re.compile('aaa\\s+[0-9]*')
    f.r2 = f.r
    l = [1, 2, 3]
    f.u = UserList([l, l])
    x = xml_pickle.dumps(f)
    print x
    g = thing_from_sax2(None, x)
    print f.u, f.r.pattern, f.r2.pattern
    return


def doit2():
    u = UserList([1, 2, [(3, 4, 5), (6, 7, 8)], 3, UserList([0, 1, 2]), 4])
    x = xml_pickle.dumps(u)
    print x
    g = thing_from_sax2(None, x)
    print g
    return


def doit(deepcopy=1):
    f = mk_foo()
    xml_pickle.setDeepCopy(deepcopy)
    print 'CREATE XML'
    t1 = time()
    fh = open('aaa.xml', 'w')
    x = xml_pickle.dump(f, fh)
    fh.close()
    print 'TIME = %f' % (time() - t1)
    print 'Pickle len = ', os.stat('aaa.xml')[ST_SIZE]
    print 'minidom pure parse'
    t1 = time()
    fh = open('aaa.xml', 'r')
    fh.close()
    print 'TIME = %f' % (time() - t1)
    print 'DOM load'
    t1 = time()
    fh = open('aaa.xml', 'r')
    xml_pickle.setParser('DOM')
    fh.close()
    print 'TIME = %f' % (time() - t1)
    print 'SAX load'
    t1 = time()
    fh = open('aaa.xml', 'r')
    xml_pickle.setParser('SAX')
    m = xml_pickle.load(fh)
    fh.close()
    print 'TIME = %f' % (time() - t1)
    del m
    print 'cEXPAT load'
    t1 = time()
    fh = open('aaa.xml', 'r')
    xml_pickle.setParser('cEXPAT')
    fh.close()
    print 'TIME = %f' % (time() - t1)


def pyxml_marshal():
    try:
        from xml.marshal import generic
    except ImportError:
        print 'Skipping PyXML xml.marshal'
        return

    f = mk_foo()
    print 'CREATE XML (xml.marshal style)'
    t1 = time()
    fh = open('bbb.xml', 'w')
    x = generic.dump(f, fh)
    fh.close()
    print 'TIME = %f' % (time() - t1)
    print 'Pickle len = ', os.stat('bbb.xml')[ST_SIZE]
    print 'xml.marshal load'
    t1 = time()
    fh = open('bbb.xml', 'r')
    m = generic.load(fh)
    fh.close()
    print 'TIME = %f' % (time() - t1)
    del m


pyxml_marshal()
doit(2)