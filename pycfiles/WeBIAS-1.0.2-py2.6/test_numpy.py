# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/webias/gnosis/xml/pickle/test/test_numpy.py
# Compiled at: 2015-04-13 16:10:48
import gnosis.xml.pickle as xml_pickle, Numeric, array, funcs
funcs.set_parser()

class foo:
    pass


f = foo()
f.a = Numeric.array([[1, 2, 3, 4], [5, 6, 7, 8]])
f.b = Numeric.array([1.2, 2.3, 3.4, 4.5])
f.y = array.array('b', [1, 2, 3, 4])
f.z = array.array('f', [1, 2, 3, 4])
a = Numeric.array([6, 7, 8, 9])

def testfoo(o1, o2):
    for attr in ['a', 'b', 'y', 'z',
     'l', 'd', 'e']:
        if getattr(o1, attr) != getattr(o2, attr):
            raise 'ERROR(1)'


f.l = [a, a, a]
f.d = {'One': a, 'Two': Numeric.array([10, 11, 12])}
f.e = f.d['Two']
x = xml_pickle.dumps(f)
g = xml_pickle.loads(x)
testfoo(f, g)
print '** OK **'