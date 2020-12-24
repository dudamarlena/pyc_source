# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/webias/gnosis/xml/pickle/test/test_gzfile.py
# Compiled at: 2015-04-13 16:10:48
import gnosis.xml.pickle as xml_pickle, gzip
from StringIO import StringIO

class C:
    pass


o = C()
o.lst, o.dct = [1, 2], {'spam': 'eggs'}
x = xml_pickle.dumps(o, 1)
sio = StringIO(x)
gz = gzip.GzipFile('dummy', 'rb', 9, sio)
if gz.read(5) != '<?xml':
    raise 'ERROR(1)'
o2 = xml_pickle.loads(x)
if o.lst != o2.lst or o.dct != o2.dct:
    raise 'ERROR(2)'
print '** OK **'