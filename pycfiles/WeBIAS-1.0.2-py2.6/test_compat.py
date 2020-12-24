# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/webias/gnosis/xml/pickle/test/test_compat.py
# Compiled at: 2015-04-13 16:10:47
import pickle, os, gnosis.xml.pickle as xml_pickle
from funcs import set_parser, unlink
set_parser()

class foo:
    pass


f = foo()
f.l = [1, 2, 3]
f.d = {'A': 1, 'B': 2, 'C': 3}
f.t = ([4, 5, 6], [7, 8, 9], [10, 11, 12])

def testfoo(o1, o2):
    for attr in ['l', 'd', 't']:
        if getattr(o1, attr) != getattr(o2, attr):
            raise 'ERROR(1)'


s = pickle.dumps(f)
x = xml_pickle.dumps(f)
g = pickle.loads(s)
testfoo(f, g)
xml_pickle.setParanoia(0)
m = xml_pickle.loads(x)
testfoo(f, m)
fh = open('aaa', 'w')
pickle.dump(m, fh)
fh.close()
fh = open('bbb', 'w')
xml_pickle.dump(m, fh)
fh.close()
fh = open('aaa', 'r')
g = pickle.load(fh)
fh.close()
testfoo(f, g)
fh = open('bbb', 'r')
g = xml_pickle.load(fh)
fh.close()
testfoo(f, g)
unlink('aaa')
unlink('bbb')
print '** OK **'