# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/webias/gnosis/xml/pickle/test/test_ftypes.py
# Compiled at: 2015-04-13 16:10:48
import pickle, test_ftypes_i, gnosis.xml.pickle as xml_pickle, funcs
funcs.set_parser()

class foo:
    pass


xml_pickle.setParanoia(0)
f = foo()
f.b = test_ftypes_i.gimme_bfunc()
f.p = test_ftypes_i.gimme_pfunc()
f.f = foo
x = xml_pickle.dumps(f)
g = xml_pickle.loads(x)
for attr in ['b', 'p', 'f']:
    if getattr(f, attr) != getattr(g, attr):
        raise 'ERROR(1)'

print '** OK **'