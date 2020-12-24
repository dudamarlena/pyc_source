# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/webias/gnosis/xml/pickle/test/test_circular.py
# Compiled at: 2015-04-13 16:10:47
import gnosis.xml.pickle as xml_pickle

class Test:
    pass


o1 = Test()
o1.s = 'o1'
o2 = Test()
o2.s = 'o2'
o1.obj1 = o2
o1.obj2 = o2
o2.obj3 = o1
o2.obj4 = o1
xml = xml_pickle.dumps(o1)
z = xml_pickle.loads(xml)
if z.s != o1.s or z.obj1.s != o1.obj1.s or z.obj2.s != o1.obj2.s or z.obj1.obj3.s != o1.obj1.obj3.s or z.obj2.obj4.s != o1.obj2.obj4.s:
    raise 'ERROR(1)'
print '** OK **'