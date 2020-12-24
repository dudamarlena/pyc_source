# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/webias/gnosis/xml/pickle/test/test_slots.py
# Compiled at: 2015-04-13 16:10:48
"""Simple __slots__ test"""
import gnosis.xml.pickle as xml_pickle, funcs
funcs.set_parser()

class foo(object):
    __slots__ = ('a', 'b')


xml_pickle.setParanoia(0)
f = foo()
f.a = 1
f.b = 2
s = xml_pickle.dumps(f)
g = xml_pickle.loads(s)
if g.__class__ != foo or g.a != f.a or g.b != f.b:
    raise 'ERROR(1)'
print '** OK **'