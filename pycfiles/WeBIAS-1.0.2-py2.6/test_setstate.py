# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/webias/gnosis/xml/pickle/test/test_setstate.py
# Compiled at: 2015-04-13 16:10:48
"""
Show that __setstate__ works by pickling the random.Random class --fpm

Note: python-2.0 lacks random, so I need another testcase for completeness
"""
import gnosis.xml.pickle as xml_pickle, sys, random, pickle
from gnosis.xml.pickle.util import setParanoia
import funcs
funcs.set_parser()

class foo:
    pass


f = foo()
x = xml_pickle.XML_Pickler(f)
r1 = random.Random(1234)
t1 = r1.random()
r1 = random.Random(1234)
r2 = random.Random(4567)
t2 = r2.random()
r2 = random.Random(4567)
r3 = random.Random(8910)
t3 = r3.random()
r3 = random.Random(8910)
r4 = random.Random(1112)
t4 = r4.random()
r4 = random.Random(1112)
f.r = r1
f.l1 = [[1, 2, 3], r2]
d = {'a': 1}
f.l2 = [r3, [4, 5, 6], r3]
f.d = {'One': 1, 'Two': r4}
setParanoia(0)
sp = pickle.dumps(f)
sx = x.dumps()
del f
g = x.loads(sx)
h = pickle.loads(sp)
p1 = g.r.random()
p2 = g.l1[1].random()
p3 = g.l2[0].random()
p4 = g.d['Two'].random()
if t1 != p1 or t2 != p2 or t3 != p3 or t4 != p4:
    raise 'ERROR(1)'
p1 = h.r.random()
p2 = h.l1[1].random()
p3 = h.l2[0].random()
p4 = h.d['Two'].random()
if t1 != p1 or t2 != p2 or t3 != p3 or t4 != p4:
    raise 'ERROR(2)'
print '** OK **'